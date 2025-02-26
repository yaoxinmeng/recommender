import time

from loguru import logger
from langchain_aws import BedrockLLM
from langchain_core.messages import SystemMessage, HumanMessage

from app.dependencies.guardrail import apply_guardrail, GuardrailException
from app.core.config import settings

RETRY_LIMIT = 10
RETRY_DELAY = 2

class LLM(BedrockLLM):
    """
    A wrapper built around LangChain's BedrockLLM class that allows us to customise some of the builtin methods.
    """
    def __init__(self):
        # Define LLM API
        kwargs = {
            "model_id": settings.BEDROCK_LLM_ID,
            "max_tokens": 1024,
            "model_kwargs": {
                "temperature": 0.2
            }
        }
        super().__init__(**kwargs)


    def invoke(self, message: HumanMessage, system_message: SystemMessage | None = None) -> str:
        """
        Custom method wrapped around LangChain's `invoke` method for customisable behaviour.

        :param HumanMessage message: The user message
        :param SystemMessage system_message: An optional system message
        :return str: The generated text from the LLM
        """
        if settings.BEDROCK_USE_GUARDRAIL:
            apply_guardrail(message.content)
        messages = [message]
        if system_message:
            messages = [system_message, message]
        for i in range(RETRY_LIMIT):
            try:
                output = super().invoke(messages)
                logger.trace(f"Generated output:\n{output}")
                if settings.BEDROCK_USE_GUARDRAIL:
                    apply_guardrail(output, False)
                return output
            except self.client.exceptions.ThrottlingException as e:  
                logger.warning(f"Failed to generate output: {e}")
                time.sleep(RETRY_DELAY * (i + 1))
            except GuardrailException as e:     # if guardrail intervened, we bubble up the error
                raise e
            except BaseException as e:
                logger.error(f"Fatal error: {e}") 
                return ""

        logger.error(f"Failed to generate output after {RETRY_LIMIT} retries")
        return ""
    
llm = LLM()