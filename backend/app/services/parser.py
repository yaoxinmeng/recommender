from typing import Any
import re
import json
from loguru import logger
from app.types.model_outputs import PreliminaryOpeningHours, PreliminaryImageData, PreliminaryLocationData


def parse_string_list(input: str) -> list[str]:
    """
    Parse the input string as a list of string.
    """
    queries = _parse_json(input)
    if not queries or type(queries) != list:
        return []
    
    results = []
    for q in queries:
        if type(q) is not str:
            continue
        results.append(q)
    return results


def parse_preliminary_location(input: str) -> PreliminaryLocationData | None:
    """
    Parse the preliminary location data into a formatted string.

    :param str input: The raw input string.
    :return: The list of formatted preliminary location data.
    """
    # Parse as json
    location = _parse_json(input)

    # validate json object
    try:
        return PreliminaryLocationData.model_validate(location)
    except:
        return None


def _parse_json(string: str) -> Any | None:
    # Parse as json
    match = re.search(r"\`\`\`json(.+)\`\`\`", string, re.DOTALL)
    if not match:
        return None
    try:
        raw_json = match.group(1).strip(" \n")
        return json.loads(raw_json)
    except:
        logger.warning("Invalid JSON object")
        return None