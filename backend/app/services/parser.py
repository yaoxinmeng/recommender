from typing import Any
import re
import json
from loguru import logger
from app.types.model_outputs import PreliminaryLocationData


def parse_string_list(input: str) -> list[str]:
    """
    Parse the input string as a list of string.
    """
    queries = _parse_json_in_backticks(input)
    # if unable to retrieve items in backticks
    if not queries or type(queries) != list:
        logger.warning("No valid JSON object found within backticks, looking for JSON object outside of backticks")
        queries = _parse_json_list(input)
    if not queries:
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
    :return: The formatted preliminary location data.
    """
    # Parse as json
    location = _parse_json_in_backticks(input)
    if not location or type(location) != dict:
        location = _parse_json_dict(input)
    logger.trace(location)
    if not location:
        return None

    # Validate the json object 
    # check basic string fields
    try:
        assert type(location["name"]) == str
        name = location["name"]
    except: name = ""
    try:
        assert type(location["address"]) == str
        address = location["address"]
    except: address = ""
    try:
        assert type(location["contact"]) == str
        contact = location["contact"]
    except: contact = ""
    try:
        assert type(location["description"]) == str
        description = location["description"]
    except: description = ""
    # check opening hours
    opening_hours = {
        "monday": {
            "start": "",
            "end": ""
        },
        "tuesday": {
            "start": "",
            "end": ""
        },
        "wednesday": {
            "start": "",
            "end": ""
        },
        "thursday": {
            "start": "",
            "end": ""
        },
        "friday": {
            "start": "",
            "end": ""
        },
        "saturday": {
            "start": "",
            "end": ""
        },
        "sunday": {
            "start": "",
            "end": ""
        }
    }
    if "opening_hours" in location:
        hours = location["opening_hours"]
        for day in opening_hours:
            if day in hours:
                try:
                    start = hours[day].get("start", "")
                    end = hours[day].get("end", "")
                    assert type(start) == str and type(end) == str 
                    opening_hours[day]["start"] = start
                    opening_hours[day]["end"] = end
                except: pass
    # check list of offerings and images
    offerings = []
    if "offerings" in location:
        for o in location["offerings"]:
            try:
                o_name = o.get("name", "")
                price = o.get("price", "")
                assert o_name and price
                assert type(o_name) == str and type(price) == str
                offerings.append({"name": o_name, "price": price})
            except: pass
    images = []
    if "images" in location:
        for i in location["images"]:
            try:
                i_name = i.get("name", "")
                url = i.get("url", "")
                assert i_name and url
                assert type(i_name) == str and type(url) == str
                if not _validate_url(url):
                    continue
                images.append({"name": i_name, "url": url})
            except: pass

    return PreliminaryLocationData(
        name=name,
        address=address,
        contact=contact,
        description=description,
        opening_hours=opening_hours,
        offerings=offerings,
        images=images
    )


def parse_image_details(input: str) -> tuple[str, list[str]]:
    """
    Parse the image details from the raw input string. Returns a tuple containing the caption
    and the list of hashtags.

    :param str input: The input string to be parsed

    :return tuple[str, list[str]]: The caption and list of hashtags extracted.
    """
    # Parse as json
    details = _parse_json_in_backticks(input)
    if not details or type(details) != dict:
        details = _parse_json_dict(input)
    logger.trace(details)
    if not details:
        return "", []
    
    caption = details.get("caption", "")
    try:
        assert type(caption) == str
    except:
        caption = ""
    hashtags = details.get("hashtags", [])
    try:
        assert type(hashtags) == list[str]
    except:
        hashtags = []
    
    return caption, hashtags


def _parse_json_in_backticks(string: str) -> Any | None:
    """
    Parse an input string and retrieve the JSON object enclosed in backticks.

    :params str string: The input string
    :returns Any | None: The parsed JSON object. If no valid objects are found, return None.
    """
    # attempt to parse string with both opening and closing backticks first
    match = re.search(r"\`\`\`json(.+?)\`\`\`", string, re.DOTALL)
    if not match:
        # attempt to parse string with only the closing backticks
        match = re.search(r"(.+)\`\`\`", string, re.DOTALL)
    if not match:
        return None
    try:
        raw_json = match.group(1).strip(" \n")
        return json.loads(raw_json)
    except:
        # for some reason LLM likes to return JSON object with an extra comma at the end
        try:
            logger.debug("Attempt json parsing with one less comma")
            removed_last_comma = "".join(list(reversed(list(reversed(raw_json)).remove(","))))
            return json.loads(removed_last_comma)
        except:
            logger.warning("Invalid JSON object found")
            return None
        

def _parse_json_list(string: str) -> list[Any] | None:
    """
    Parse an input string and retrieve the JSON list.

    :params str string: The input string
    :returns list[Any] | None: The parsed JSON list. If no valid objects are found, return None.
    """
    match = re.search(r"(\[.+\])", string, re.DOTALL)
    if not match: 
        return None
    try:
        raw_json = match.group(1).strip(" \n")
        return json.loads(raw_json)
    except:
        logger.warning("Invalid JSON object found")
        return None
        

def _parse_json_dict(string: str) -> dict[str, Any] | None:
    """
    Parse an input string and retrieve the JSON object.

    :params str string: The input string
    :returns dict[str, Any] | None: The parsed JSON object. If no valid objects are found, return None.
    """
    match = re.search(r"(\{.+\})", string, re.DOTALL)
    if not match: 
        return None
    try:
        raw_json = match.group(1).strip(" \n")
        return json.loads(raw_json)
    except:
        logger.warning("Invalid JSON object found")
        return None


def _validate_url(string: str) -> bool:
    """
    Verify that the input string is a valid url
    """
    match = re.findall(r"https?:\/\/.*", string)
    if not match:
        return False
    return True