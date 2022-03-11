import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from utils import *
from api import run_api

load_dotenv()

TOKEN = os.environ["TOKEN"]

client = commands.Bot(">", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_presence_update(before, after):
    """
    Called when a person updates their presence
    """

    activity, status = None, None

    # Activity
    if after.activity is None:
        activity = "None"

    elif before.activity is None and after.activity is not None:
        activity = after.activity.name

    elif before.activity is not None and after.activity is not None and before.activity != after.activity:
        activity = after.activity.name


    # Status
    if after.status is None:
        status = "None"

    elif before.status is None and after.status is not None:
        status = str(after.status)

    elif before.status is not None and after.status is not None and before.status != after.status:
        status = str(after.status)

    
    # Update database files:
    await update_status(after.id, status)
    await update_activity(after.id, activity)


# on join - add to db

# if not in db print user not in db

# on leave - delete from db


run_api()
client.run(TOKEN)