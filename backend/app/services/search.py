from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

from loguru import logger

from app.core.config import settings
from app.types.search import SearchResults


class Search:
    def __init__(self):
        # Define web search API wrapper for DuckDuckGo
        # Set the default region to Singapore and the default time to the past year
        self.wrapper = DuckDuckGoSearchAPIWrapper(region="sg-en", time="y")

    
    def search_query(self, query: str, n_results: int) -> list[SearchResults]:
        search = DuckDuckGoSearchResults(api_wrapper=self.wrapper, output_format="list", max_results=n_results)
        raw_results = search.invoke(query + " Singapore")   # needed because results are still not geolocated
        results = [SearchResults.model_validate(r) for r in raw_results]
        logger.debug(f"Retrieved the following results for search query '{query}': {[r.title for r in results]}")
        return results
    
search = Search()