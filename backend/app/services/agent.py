from loguru import logger
from langchain_core.messages import HumanMessage

from app.services.search import search
from app.services.scraper import scraper
from app.dependencies.multimodal_llm import multimodal_llm
from app.types.schema import LocationData
from app.types.search import SearchResults

def venue_agent(query: str, n_results: int) -> list[LocationData]:
    # get the relevant results from live web search
    relevant_results = search.search_query(query, n_results)
    logger.trace(relevant_results)

    # scrape information from the relevant web pages
    location_data: list[LocationData] = []
    for page in relevant_results:
        content = scraper.scrape_basic_location(page.link)
        # convert the basic location data to preliminary location data
        parsed_content = [LocationData(
            name=location.name, 
            address=location.address, 
            opening_hours={}, 
            description=location.description,
            offerings={},
            contact=location.contact,
            images={},
            citation=[page.link],
            ) for location in content]
        location_data.extend(parsed_content)
        if len(location_data) >= n_results:
            break

    # retain unique locations
    location_data = list({(location.name): location for location in location_data}.values())
    location_data = location_data[:n_results]
    logger.trace(location_data)

    # retrieve the remaining information by performing specific web searches
    for location in location_data:
        # get opening hours
        relevant_results = search.search_query(location.name + " opening hours", n_results)
        logger.trace(relevant_results)
        

    return location_data


def generate_caption(image_base64: str, format: str) -> str:
    """
    Use LLM to transform the tone of the image caption.
    """
    # TODO: Implement the prompt template for this function
    caption = multimodal_llm.invoke(HumanMessage(
        content=[
            {"text": "Caption this image in less than 70 words"},
            {"image": {"format": format, "source": {"bytes": image_base64}}},
        ],
    ))
    return caption