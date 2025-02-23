import time

from loguru import logger
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

from app.types.search import SearchResults

wrapper = DuckDuckGoSearchAPIWrapper(region="sg-en", time="y")

RETRIES = 3
BACKOFF = 2

def search_duckduckgo(query: str, max_results: int = 3) -> list[str]:
    """
    Call to perform a web search of the query.

    :param str query: The search query.
    :return: The list of relevant URLs.
    """
    search = DuckDuckGoSearchResults(api_wrapper=wrapper, output_format="list", max_results=max_results)
    for i in range(RETRIES + 1):
        try:
            raw_results = search.invoke(query)
            results = [SearchResults.model_validate(r) for r in raw_results]
            return [result.link for result in results]
        except Exception as e:
            logger.error(f"Failed to retrieve search results: {e}")
            time.sleep((i + 1) * BACKOFF)
    
    return []