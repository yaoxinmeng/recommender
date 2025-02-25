import base64
import os
import subprocess
import requests

from langchain_core.messages import HumanMessage
from loguru import logger

from app.dependencies.multimodal_llm import multimodal_llm
from app.services.prompts import IMAGE_CAPTION_PROMPT, STRUCTURED_RESPONSE_SYSTEM_PROMPT
from app.services.parser import parse_image_details
from app.types.model_json_schema import IMAGE_DETAILS_JSON_SCHEMA
from app.types.schema import ImageData

def generate_caption_hashtags(image_data: ImageData) -> tuple[str, list[str]]:
    """
    Use LLM to caption the provided image based on guided tones.
    """
    # retrieve image
    r = requests.get(image_data.url)
    try:
        r.raise_for_status()
    except:
        logger.error(f"Unable to retrieve image data from url {image_data.url}")
        return "", []

    # convert to PNG and encode as base64
    image_base64 = _generate_base64_from_url(image_data.url)
    if not image_base64:
        return "", []

    # generate image caption and hashtags
    output = multimodal_llm.invoke(HumanMessage(
        content=[
            {"text": IMAGE_CAPTION_PROMPT},
            {"image": {"format": "png", "source": {"bytes": image_base64}}},
        ]),
        system_message=STRUCTURED_RESPONSE_SYSTEM_PROMPT.format(json_schema=IMAGE_DETAILS_JSON_SCHEMA)
    )
    caption, hashtags = parse_image_details(output)
    return caption, hashtags


def _generate_base64_from_url(url: str) -> str:
    """
    Attempts to retrieve an image from any url and encode as PNG. Returns the base64 representation of the image.

    :param str url: The url of the image
    :return str: The base64 string
    """
    # retrieve image
    r = requests.get(url)
    try:
        r.raise_for_status()
    except:
        logger.error(f"Unable to retrieve image data from url {url}")
        return ""
    
    # write to local temporary file
    if not os.path.exists("temp"):
        os.mkdir("temp")
    image_name = url.split("/")[-1]
    file_name = os.path.join("temp", image_name)
    with open(file_name, "wb") as f:
        f.write(r.content)

    # use ffmpeg to convert to standard png format
    output_name = os.path.splitext(file_name)[0] + "-temp.png"
    try:
        subprocess.check_call([
            "ffmpeg", "-y",
            "-i", file_name,
            output_name
        ])
        os.remove(file_name)
    except subprocess.CalledProcessError as e:
        logger.warning(f"Failed to convert file with ffmpeg : {e}")
        os.remove(file_name)
        return ""
    
    # encode image as base64 string
    with open(output_name, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("ascii")
    os.remove(output_name)
    return image_base64