import traceback

from fastapi import APIRouter, HTTPException
from loguru import logger

from app.types.payload import SearchPayload
from app.services.agent import extract_locations
from app.types.schema import LocationData

router = APIRouter()

@router.post(path="/venues", response_model=list[LocationData])
def search_venues(body: SearchPayload) -> list[LocationData]:
    try:
        locations = extract_locations(body.query, body.num_results, body.num_iterations)
        return locations
    # the only uncaight exception that should bubble up here is the guardrails intervention
    except BaseException as e:
        logger.error(traceback.format_exc())
        raise HTTPException(400, repr(e))