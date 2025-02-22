from pydantic import BaseModel

class SearchResults(BaseModel):
    """
    Information relating to a single search result.

    :params str snippet: A short preview of the web page
    :params str title: The title of the web page
    :params str url: The link to the web page
    """
    snippet: str
    title: str
    link: str