from loguru import logger
import sys 
from app.core.config import settings

def config_logger():
    if settings.ENV == "debug":
        level = "TRACE"
    elif settings.ENV == "dev":
        level = "DEBUG"
    elif settings.ENV == "prod":
        level = "INFO"
    else:
        level = "INFO"

    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - {message}",
        level=level
    )

    # remove default logger, if it exists
    try:
        logger.remove(0)
    except ValueError:
        logger.info('Failed to remove default logger because it does not exist.')
    except:
        logger.error("Fatal exception encountered while attempting to remove default logger.")
