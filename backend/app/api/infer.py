from fastapi import APIRouter
from app.types.payload import SearchPayload
from app.services.agent import venue_agent
from app.types.schema import LocationData

router = APIRouter()

@router.post(path="/venues", response_model=list[LocationData])
def search_venues(body: SearchPayload) -> list[LocationData]:
    return venue_agent(body.query, body.num_results)