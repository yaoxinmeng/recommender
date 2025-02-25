import json
import time

from langchain_core.messages import HumanMessage
from loguru import logger
import boto3

from app.core.config import settings

RETRY_LIMIT = 10
RETRY_DELAY = 2

class MultimodalLLM:
    """
    A custom class that does not use LangChain since it currently does not support Amazon Nova input schema.
    """
    def __init__(self):
        # Define LLM API
        self.client = boto3.client(
            "bedrock-runtime"
        )

    def invoke(self, message: HumanMessage, system_message: str = "", **kwargs) -> str:
        """
        Custom invoke method to generate debug logs based on environment settings.
        """
        request_body = {
            "schemaVersion": "messages-v1",
            "messages": [
                {"role": "user", "content": message.content}
            ],
            "inferenceConfig": kwargs,
        }
        if system_message:
            request_body["system"] = [{"text": system_message}]

        for i in range(RETRY_LIMIT):
            try:
                response = self.client.invoke_model_with_response_stream(
                    modelId=settings.BEDROCK_MULTIMODAL_ID, body=json.dumps(request_body)
                )
                # Process the response stream
                stream = response.get("body")
                if stream:
                    content = ""
                    for event in stream:
                        chunk = event.get("chunk")
                        if chunk:
                            chunk_json = json.loads(chunk.get("bytes").decode())
                            try:
                                content_chunk = chunk_json["contentBlockDelta"]["delta"]["text"]
                                if content_chunk:
                                    content += content_chunk
                            except: pass
                else:
                    logger.warning("No response stream received.")
                    return ""
                logger.trace(f"Generated output:\n{content}")
                return content
            except Exception as e:
                logger.warning(f"Failed to generate output: {e}")
                time.sleep(RETRY_DELAY * (i + 1))

        logger.error(f"Failed to generate output after {RETRY_LIMIT} retries")
        return ""
    
multimodal_llm = MultimodalLLM()