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


def autorole():
    return os.environ.get('AUTOROLE')


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

    @client.event
    async def on_member_join(member):
        role_name = autorole()
        if not role_name:
            logger.info(f"No autorole found for new member {member.name}.")
            return
        role = discord.utils.get(member.guild.roles, name=role_name)
        if not role:
            logger.info(f"{role_name} role not found! New member {member.name} not assigned.")
            return
        await member.add_roles(role)
        logger.info(f"New member {member.name} assigned {role_name}.")


    client.run(token(), log_level=logging.INFO)
