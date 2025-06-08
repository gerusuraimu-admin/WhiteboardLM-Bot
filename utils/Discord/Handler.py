import discord
from utils import get_logger
from utils.Common import respond
from utils.Discord.DiscordEventObject import DiscordEventObject


def discord_start(token: str, uid: str):
    logger = get_logger('Discord')
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    def from_user(obj: DiscordEventObject) -> bool:
        return obj.author != client.user or client.user in obj.mentions

    @client.event
    async def on_ready():
        logger.info(f'Bot Start: {uid}')

    @client.event
    async def on_message(message):
        obj = DiscordEventObject(message)

        if from_user(obj):
            logger.info(f'Message from {uid}')
            result = respond(obj.message, uid)
            await obj.channel.send(result)

    client.run(token)
