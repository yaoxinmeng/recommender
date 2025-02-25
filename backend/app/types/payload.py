from pydantic import BaseModel

class SearchPayload(BaseModel):
    """
    :params str query: The search query from the user
    :params int num_results: The number of relevant results expected by the user. If not provided, the default is 10.
    """
    query: str
    num_results: int = 10
    num_iterations: int = 2