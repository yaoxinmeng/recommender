import json

from loguru import logger
from langchain_core.messages import SystemMessage, HumanMessage

from app.dependencies.llm import llm
from app.types.model_outputs import PreliminaryLocationData
from app.types.model_json_schema import PRELIMINARY_LOCATION_JSON_SCHEMA
from app.services.prompts import STRUCTURED_OUTPUT_PROMPT, CANDIDATE_LOCATIONS_PROMPT, SEARCH_QUERY_PROMPT, STRUCTURED_OUTPUT_SYSTEM_PROMPT, STRUCTURED_RESPONSE_SYSTEM_PROMPT
from app.services.parser import parse_preliminary_location, parse_string_list


def get_preliminary_location(text: str, location_name: str) -> PreliminaryLocationData | None:
    messages = [
        SystemMessage(STRUCTURED_OUTPUT_SYSTEM_PROMPT.format(
            json_schema=PRELIMINARY_LOCATION_JSON_SCHEMA
        )),
        HumanMessage(STRUCTURED_OUTPUT_PROMPT.format(
            text=text.strip(" \n"),
            name=location_name
        ))
    ]
    logger.trace(messages)
    content = llm.invoke(messages)
    return parse_preliminary_location(content)


def get_candidate_locations(text: str, query: str) -> list[str]:
    messages = [
        SystemMessage(STRUCTURED_RESPONSE_SYSTEM_PROMPT.format(
            json_schema='[\n"<location_or_event_name>"\n]'
        )),
        HumanMessage(CANDIDATE_LOCATIONS_PROMPT.format(
            query=query, 
            text=text
        ))
    ]
    logger.trace(messages)
    output = llm.invoke(messages)
    locations = parse_string_list(output)
    refined_locations = list(filter(lambda x: not x.startswith("<"), locations))
    return refined_locations
    

def get_search_queries(query: str, location: PreliminaryLocationData):
    messages = [
        SystemMessage(STRUCTURED_RESPONSE_SYSTEM_PROMPT.format(
            json_schema='{[\n"<search_query>"\n]}'
        )),
        HumanMessage(SEARCH_QUERY_PROMPT.format(
            query=query,
            information=json.dumps(location.model_dump(mode="json")),
            schema=PRELIMINARY_LOCATION_JSON_SCHEMA
        ))
    ]
    logger.trace(messages)
    content = llm.invoke(messages)
    queries = parse_string_list(content)
    refined_queries = list(filter(lambda x: not x.startswith("<"), queries))
    return refined_queries