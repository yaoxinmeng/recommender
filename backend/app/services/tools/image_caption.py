from langchain_core.messages import SystemMessage, HumanMessage
import requests
from loguru import logger
import base64

from app.dependencies.multimodal_llm import multimodal_llm
from app.types.schema import ImageData

def generate_caption(image_name: str, image_data: ImageData) -> str:
    """
    Use LLM to caption the provided image based on guided tones.
    """
    # retrieve image
    r = requests.get(image_data.url)
    try:
        r.raise_for_status()
    except:
        logger.error(f"Unable to retrieve image data from url {image_data.url}")
        return ""

    # convert to base64
    image_base64 = base64.b64encode(r.content)
    image_format = image_data.url.split(".")[-1]

    # TODO: Implement the prompt template for this function
    caption = multimodal_llm.invoke(HumanMessage(
        content=[
            {"text": "Caption this image in less than 70 words"},
            {"image": {"format": image_format, "source": {"bytes": image_base64}}},
        ],
    ))
    return caption