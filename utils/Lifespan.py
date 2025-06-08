from contextlib import asynccontextmanager
from fastapi import FastAPI
from utils.Logger import get_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = get_logger('Lifespan')
    logger.info(f'Start Bot Server: {app}')

    yield

    logger.info(f'End Bot Server: {app}')
