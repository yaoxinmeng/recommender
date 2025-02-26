import time

from loguru import logger
from langchain_aws import BedrockLLM
from langchain_core.callbacks import AsyncCallbackHandler

from app.core.config import settings

class BedrockAsyncCallbackHandler(AsyncCallbackHandler):
    # Async callback handler that can be used to handle callbacks from langchain.
    async def on_llm_error(self, error: BaseException, **kwargs) -> None:
        reason = kwargs.get("reason")
        if reason == "GUARDRAIL_INTERVENED":
            logger.warning(f"Guardrails: {kwargs}")


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
        if settings.BEDROCK_USE_GUARDRAIL:
            super().__init__(
                guardrails={"id": settings.BEDROCK_GUARDRAIL_ID, "version": settings.BEDROCK_GUARDRAIL_VERSION, "trace": True},
                callbacks=[BedrockAsyncCallbackHandler()],
                **kwargs
            )
        else:
            super().__init__(**kwargs)

    def invoke(self, *args, **kwargs) -> str:
        """
        Custom invoke method to generate debug logs based on environment settings.
        """
        for i in range(RETRY_LIMIT):
            try:
                output = super().invoke(*args, **kwargs)
                logger.trace(f"Generated output:\n{output}")
                return output
            except self.client.exceptions.ThrottlingException as e:  
                logger.warning(f"Failed to generate output: {e}")
                time.sleep(RETRY_DELAY * (i + 1))
            except Exception as e:
                logger.error(f"Fatal error: {e}") 
                return ""

        logger.error(f"Failed to generate output after {RETRY_LIMIT} retries")
        return ""
    
llm = LLM()