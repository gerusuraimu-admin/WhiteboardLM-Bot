from logging import Logger
from fastapi import FastAPI
from utils import (
    handle_wrapper,
    get_logger,
    get_server,
    ProcessManager,
    UIDPayload,
    App
)

logger: Logger = get_logger(__name__)
server: FastAPI = get_server()
manager = ProcessManager()


@server.post('/slack_bot/run')
@handle_wrapper
async def slack_run(payload: UIDPayload):
    logger.info('Slack Bot Start')
    manager.run(payload.uid, App.slack)


@server.post('/slack_bot/stop')
@handle_wrapper
async def slack_stop(payload: UIDPayload):
    logger.info('Slack Bot Stop')
    manager.stop(payload.uid, App.slack)


@server.post('/discord_bot/run')
@handle_wrapper
async def discord_run(payload: UIDPayload):
    logger.info('Discord Bot Start')
    manager.run(payload.uid, App.discord)


@server.post('/discord_bot/stop')
@handle_wrapper
async def discord_stop(payload: UIDPayload):
    logger.info('Discord Bot Stop')
    manager.stop(payload.uid, App.discord)
