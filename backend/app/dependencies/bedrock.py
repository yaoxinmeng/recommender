from langchain_aws import BedrockLLM, ChatBedrock
from langchain_core.callbacks import AsyncCallbackHandler

from loguru import logger

from app.core.config import settings

class BedrockAsyncCallbackHandler(AsyncCallbackHandler):
    # Async callback handler that can be used to handle callbacks from langchain.
    async def on_llm_error(self, error: BaseException, **kwargs) -> None:
        reason = kwargs.get("reason")
        if reason == "GUARDRAIL_INTERVENED":
            logger.warning(f"Guardrails: {kwargs}")

class Bedrock(BedrockLLM):
    """
    A wrapper built around LangChain's BedrockLLM class that allows us to customise some of the builtin methods.
    """
    def __init__(self):
        # Define LLM API
        if settings.BEDROCK_USE_GUARDRAIL:
            super().__init__(
                model_id=settings.BEDROCK_LLM_ID,
                guardrails={"id": settings.BEDROCK_GUARDRAIL_ID, "version": settings.BEDROCK_GUARDRAIL_VERSION, "trace": True},
                callbacks=[BedrockAsyncCallbackHandler()],
                beta_use_converse_api=True,
            )
        else:
            super().__init__(
                model_id=settings.BEDROCK_LLM_ID,
                beta_use_converse_api=True,
            )

    def invoke(self, *args, **kwargs) -> str:
        """
        Custom invoke method to generate debug logs based on environment settings.
        """
        output = super().invoke(*args, **kwargs)
        logger.trace(f"Generated output:\n{output}")
        return output
    
llm = Bedrock()