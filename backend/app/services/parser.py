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
    :return: The formatted preliminary location data.
    """
    # Parse as json
    location = _parse_json(input)
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
                name = o.get("name", "")
                price = o.get("price", "")
                assert name and price
                assert type(name) == str and type(price) == str
                offerings.append({"name": name, "price": price})
            except: pass
    images = []
    if "images" in location:
        for i in location["images"]:
            try:
                name = i.get("name", "")
                url = i.get("url", "")
                hashtags = i.get("hashtags", [])
                assert name and url
                assert type(name) == str and type(url) == str and type(hashtags) == list
                for h in hashtags:
                    assert type(h) == str
                images.append({"name": name, "url": url, "hashtags": hashtags})
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


def _parse_json(string: str) -> Any | None:
    # Parse as json
    match = re.search(r"\`\`\`json(.+?)\`\`\`", string, re.DOTALL)
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