from fastapi import APIRouter
from app.types.payload import SearchPayload
from app.services.agent import extract_locations
from app.types.schema import LocationData

router = APIRouter()

@router.post(path="/venues", response_model=list[LocationData])
def search_venues(body: SearchPayload) -> list[LocationData]:
    return extract_locations(body.query, body.num_results, body.num_iterations)