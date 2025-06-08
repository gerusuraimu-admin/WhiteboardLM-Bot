from itertools import chain
from typing import Dict, Optional
from threading import Lock
from multiprocessing import Process
from google.cloud import firestore
from utils.Common.Payload import App
from utils.Logger import get_logger
from utils.Discord.Handler import discord_start
from utils.Slack.Handler import slack_start


class ProcessManager:
    _lock = Lock()
    _instance: Optional['ProcessManager'] = None

    def __init__(self) -> None:
        self.db = firestore.Client()
        self.logger = get_logger('ProcessManager')
        self.discord: Dict[str, Process] = dict()
        self.slack: Dict[str, Process] = dict()

    def __new__(cls, *args, **kwargs) -> 'ProcessManager':
        if cls._instance is None:
            with cls._lock:
                cls._instance = super().__new__(cls)
        return cls._instance

    def shutdown(self) -> None:
        for p in chain(self.discord.values(), self.slack.values()):
            self.terminate(p)

    def run(self, uid: str, app: App) -> None:
        with self._lock:
            doc_ref = self.db.collection(f'tokens_{app.value}').document(uid)
            doc = doc_ref.get()
            if not doc.exists:
                raise Exception(f'Doc {uid} does not exist')
            tokens = doc.to_dict()

            if app == App.discord:
                if uid in self.discord:
                    raise Exception(f'Discord {uid} already exists')
                discord_token = tokens.get('discordToken')
                p = Process(target=discord_start, args=(discord_token, uid))
                self.discord[uid] = p
                p.start()
            elif app == App.slack:
                if uid in self.slack:
                    raise Exception(f'Slack {uid} already exists')
                slack_token = tokens.get('slackToken')
                app_token = tokens.get('appToken')
                p = Process(target=slack_start, args=(slack_token, app_token, uid))
                self.slack[uid] = p
                p.start()

    def stop(self, uid: str, app: App) -> None:
        with self._lock:
            if app == App.discord:
                if uid not in self.discord:
                    raise Exception(f'Discord {uid} does not exist')
                self.terminate(self.discord[uid])
                del self.discord[uid]
            elif app == App.slack:
                if uid not in self.slack:
                    raise Exception(f'Slack {uid} does not exist')
                self.terminate(self.slack[uid])
                del self.slack[uid]

    def terminate(self, p: Process, timeout: int = 3) -> None:
        if p.is_alive():
            p.kill()
            p.join(timeout)
            if p.is_alive():
                self.logger.error(f'Failed to kill process: {p.name}')
            else:
                self.logger.info(f'Process {p.name} killed')
