import os
import asyncio
import discord
from utils import Card
from dotenv import load_dotenv
from discord.ext import commands
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, RedirectResponse, JSONResponse
from datetime import datetime
from babel.dates import format_datetime

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

load_dotenv()

TOKEN = os.environ["TOKEN"]

URL = "https://discordimage.herokuapp.com"

intents = discord.Intents.all()
intents.presences = True
intents.members = True


client = commands.Bot(">", intents=intents, help_command=None)

# Description for api docs
description = """
### Made by FusionSid

[My Github](https://github.com/FusionSid)

This api lets you generate an image of your discord
Make sure to join the [discord](https://discord.gg/p9GuT5hakm) For this to work

#### Source Code:
[https://github.com/FusionSid/DiscordStatusAPI](https://github.com/FusionSid/DiscordPresenceAPI)

#### Contact:
Discord: FusionSid#3645

#### LICENCE:
"""

# Creates an instance of the FastAPI class
app = FastAPI(
    title = "DiscordStatusAPI",
    description=description,
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@client.event
async def on_ready():
    print("Bot is ready!")


@app.get("/api/image", responses = {200: {"content": {"image/png": {}}}, 404 : {"content" : {"application/json":{}}}}, response_class=StreamingResponse)
@limiter.limit("30/minute")
async def image(request : Request, user_id : int, rounded_corners : bool = True, resize_width : int = None):
    main_guild = client.get_guild(942546789372952637)
    
    try:
        user = await main_guild.fetch_member(user_id)
    except Exception as error:
        if isinstance(error, discord.errors.NotFound):
        
            if error.code == 10007:
                guild_2 = client.get_guild(763348615233667082)
                try:
                    user = await guild_2.fetch_member(user_id)
                    main_guild = guild_2
                except discord.errors.NotFound as error_2:
                    if error_2.code == 10007:
                        return JSONResponse(content={"error" : f"{error}", "fix" : "Make sure you are in the guild: https://discord.gg/p9GuT5hakm"}, status_code=404)

            if error.code == 10013:
                return JSONResponse(content={"error" : f"{error}", "fix" : "Make sure user_id is correct"}, status_code=404)

        else:
            print(error)
            return error

    user = main_guild.get_member(user_id)
            
    card = Card(user, rounded_corner=rounded_corners, resize_length=resize_width)

    if user.activity is None:
        image = await card.status_image()
    else:
        image = await card.status_image()
        
    now = datetime.utcnow()
    format = 'EEE, dd LLL yyyy hh:mm:ss'
    timern = format_datetime(now, format, locale='en') + ' GMT'
    headers = {"Cache-Control" : "no-cache", "Expires" : timern}
    return StreamingResponse(image, 200, media_type="image/png", headers=headers)

@client.command()
async def help(ctx):
    em = discord.Embed(title="Discord Status API", description=f"Join the [discord](https://discord.gg/p9GuT5hakm)\n[Read The Docs]({URL}/docs)", color=discord.Color.blue())
    em.add_field(name="Usage", value=f"{URL}/api/image?user_id={ctx.author.id}")
    await ctx.send(embed=em)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.errors.NotFound):
        
        if error.code == 10007:
            pass

        if error.code == 10013:
            pass

    else:
        print(error)


@app.get("/discord")
async def discord_server():
    return RedirectResponse("https://discord.gg/p9GuT5hakm")


@app.get("/")
async def home():
    return {
        "docs" : f"{URL}/docs",
        "Join the discord for this to work" : "https://discord.gg/p9GuT5hakm"
    }


@app.on_event("startup")
async def startup_event():
  asyncio.create_task(client.start(TOKEN))