from enum import Enum
from pydantic import BaseModel


class App(Enum):
    discord = 'discord'
    slack = 'slack'


class UIDPayload(BaseModel):
    uid: str
