from pydantic import BaseModel, Field

class SearchResults(BaseModel):
    snippet: str = Field(description="A short preview of the web page")
    title: str = Field(description="The title of the web page")
    link: str = Field(description="The link to the web page")