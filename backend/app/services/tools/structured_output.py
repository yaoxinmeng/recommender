import json

from loguru import logger
from langchain_core.messages import SystemMessage, HumanMessage

from app.dependencies.llm import llm
from app.types.model_outputs import PreliminaryLocationData
from app.types.model_json_schema import PRELIMINARY_LOCATION_JSON_SCHEMA
from app.services.prompts import (
    PRELIMINARY_INFORMATION_PROMPT, 
    CANDIDATE_LOCATIONS_PROMPT, 
    SEARCH_QUERY_PROMPT, 
    STRUCTURED_OUTPUT_SYSTEM_PROMPT, 
    STRUCTURED_RESPONSE_SYSTEM_PROMPT, 
    COMPARE_INFORMATION_PROMPT)
from app.services.parser import parse_preliminary_location, parse_string_list


def get_preliminary_location(text: str, location_name: str) -> PreliminaryLocationData | None:
    """
    Extract information of the provided location from the input text.

    :param str text: The raw text to extract information from
    :param str location_name: The name of the location of interest
    :return PreliminaryLocationData | None: If no information is found, return None.
    """
    prompt = PRELIMINARY_INFORMATION_PROMPT.format(
        text=text.strip(" \n"),
        name=location_name
    )
    system_prompt = STRUCTURED_OUTPUT_SYSTEM_PROMPT.format(
        json_schema=PRELIMINARY_LOCATION_JSON_SCHEMA
    )
    logger.trace(prompt)
    content = llm.invoke(HumanMessage(prompt), SystemMessage(system_prompt))
    return parse_preliminary_location(content)


def get_candidate_locations(text: str, query: str) -> list[str]:
    """
    Extract locations that are relevant to the query from the input text.

    :param str text: The input text 
    :param str query: The user query
    :return list[str]: The list of candidate locations 
    """
    prompt = CANDIDATE_LOCATIONS_PROMPT.format(
        query=query, 
        text=text
    )
    logger.trace(prompt)
    output = llm.invoke(HumanMessage(prompt))
    locations = parse_string_list(output)
    refined_locations = list(filter(lambda x: not x.startswith("<"), locations))
    return refined_locations
    

def get_search_queries(location_name: str, location: PreliminaryLocationData) -> list[str]:
    """
    Generate a list of logical search queries to fill the missing information in 
    the current location object.

    :param str location_name: The name of the location
    :param PreliminaryLocationData location: The current information of the location
    :return list[str]: The list of search queries
    """
    prompt = SEARCH_QUERY_PROMPT.format(
        query=location_name,
        information=json.dumps(location.model_dump(mode="json")),
    )
    logger.trace(prompt)
    content = llm.invoke(HumanMessage(prompt))
    queries = parse_string_list(content)
    refined_queries = list(filter(lambda x: not x.startswith("<"), queries))
    return refined_queries


def update_location_data(old_data: PreliminaryLocationData, new_data: PreliminaryLocationData | None) -> PreliminaryLocationData:
    """
    Update the old location data with field(s) from the new location data. 

    :param PreliminaryLocationData old_data: The old location data
    :param PreliminaryLocationData new_data: The newly generated location data
    :return PreliminaryLocationData: The combined location data
    """
    prompt = COMPARE_INFORMATION_PROMPT.format(
        document_1=old_data.model_dump_json(),
        document_2=new_data.model_dump_json()
    )
    system_prompt = STRUCTURED_RESPONSE_SYSTEM_PROMPT.format(
        json_schema=PRELIMINARY_LOCATION_JSON_SCHEMA
    )
    logger.trace(prompt)
    content = llm.invoke(HumanMessage(prompt), SystemMessage(system_prompt))
    return parse_preliminary_location(content)