import datetime
import discord
import os
import logging
import time
from discord.ext import commands
from discord.ext import tasks
from pathlib import Path

from db import set_token
from db import get_token


logger = logging.getLogger()


def token():
    token = os.environ.get('TOKEN')
    if token:
        set_token(token)
    token = get_token()
    if not token:
        raise Exception("No token found!")
    return token

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix='.', intents=intents)
    start_time = time.time()

    @client.event
    async def on_ready():
        logger.info(f"{client.user} has connected to Discord!")
    
    @client.command(aliases=["ms","latency"]) #ping latency cmd
    async def ping(ctx):
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - start_time))))
        latency = round(client.latency * 100)
        await ctx.send(f"{ latency }ms, uptime { uptime }")

    client.run(token(), log_level=logging.INFO)
