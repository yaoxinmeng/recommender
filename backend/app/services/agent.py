from app.dependencies.bedrock import llm
from app.services.search import search
from app.services.scraper import scraper
from app.types.schema import LocationData
from app.types.search import SearchResults

def venue_agent(query: str, n_results: int) -> list[LocationData]:
    # get the relevant results from live web search
    relevant_results = search.search_query(query, n_results)

    # determine the relevant web pages
    relevant_pages = relevant_web_pages(relevant_results)

    # scrape information from the relevant web pages
    location_data = [scraper.scrape_with_playwright(page) for page in relevant_pages]

    # transform the tone of the image captions
    for i, data in enumerate(location_data):
        for name in data.images:
            location_data[i].images[name].caption = transform_tone(data.images[name].caption)
    return location_data
            

def relevant_web_pages(relevant_results: list[SearchResults]) -> list[str]:
    """
    Use LLM to determine the most relevant web pages from the search results.
    """
    # TODO: Implement the prompt template for this function
    return [r.link for r in relevant_results]


def transform_tone(caption: str) -> str:
    """
    Use LLM to transform the tone of the image caption.
    """
    # TODO: Implement the prompt template for this function
    return caption