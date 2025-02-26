from fastapi import APIRouter

router = APIRouter()

@router.get(path="/", response_model=str)
def health_check() -> str:
    return "OK"