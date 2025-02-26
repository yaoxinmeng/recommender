from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.logging import config_logger
from app.api import infer, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application dependencies
    """
    config_logger()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(health.router, prefix="/health", tags=["Misc"])
app.include_router(infer.router, prefix="/infer", tags=["Infer"])
