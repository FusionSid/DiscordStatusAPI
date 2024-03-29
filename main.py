import os
import asyncio
from io import BytesIO
from datetime import datetime

import shlex
import discord
from dotenv import load_dotenv
from discord.ext import commands
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, RedirectResponse, JSONResponse
import aiohttp
from babel.dates import format_datetime
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from utils import Card


limiter = Limiter(key_func=get_remote_address)

load_dotenv()

TOKEN = os.environ["TOKEN"]

URL = "https://readme-stats.herokuapp.com"

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
async def image(request : Request, user_id : int, rounded_corners : bool = True, show_activity : bool = True, resize_width : int = 450, show_hypesquad : bool = True, name_color : str = "white", discriminator_color : str= "white", activity_color : str= "white", background_color : str= "#161a1d"):
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

    card = Card(user, rounded_corner=rounded_corners, resize_length=resize_width, name_color=name_color, discriminator_color=discriminator_color, background_color=background_color, activity_color=activity_color, show_hypesquad=show_hypesquad)

    if user.activity is not None and show_activity is True:
        image = await card.activity_image()
    else:
        image = await card.status_image()

    now = datetime.utcnow()
    format = 'EEE, dd LLL yyyy hh:mm:ss'
    timern = format_datetime(now, format, locale='en') + ' GMT'
    headers = {"Cache-Control" : "no-cache", "Expires" : timern}
    return StreamingResponse(image, 200, media_type="image/png", headers=headers)


@app.get("/discord")
async def discord_server():
    return RedirectResponse("https://discord.gg/p9GuT5hakm")


@app.get("/")
async def home():
    return RedirectResponse("/docs")


# Discord bot stuff:

@app.on_event("startup")
async def startup_event():
  asyncio.create_task(client.start(TOKEN))


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


@client.command()
async def image(ctx, member : discord.Member = None):
    if member is None:
        member = ctx.author

    url = f"https://readme-stats.herokuapp.com/api/image?user_id={member.id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            image = await resp.read()

    file = BytesIO(image)
    file.seek(0)
    await ctx.send(file=discord.File(file, "card.png"))


@client.command(aliases=["gen_url", "url"])
async def gen_image(ctx, member : discord.Member, *, kwargs = None):

    url = f"https://readme-stats.herokuapp.com/api/image?user_id={member.id}"

    if kwargs is not None:
        kwargs = shlex.split(kwargs)
        args = {}

        for index in range(len(kwargs)):
            if index % 2 == 0:
                args[kwargs[index].lstrip("--")] = kwargs[index+1]
            index += 0

        for key, value in args.items():
            if key.lower() == "name_color":
                url += f"&name_color={value}"

            elif key.lower() == "bg_color":
                url += f"&background_color={value}"

            elif key.lower() == "d_color" or key.lower() == "discriminator_color":
                url += f"&discriminator_color={value}"

            elif key.lower() == "show_activity" or key.lower() == "activity":
                url += f"&show_activity={value}"

            elif key.lower() == "rounded" or key.lower() == "rounded_corners":
                url += f"&rounded_corners={value}"

            elif key.lower() == "resize" or key.lower() == "resize_width":
                url += f"&resize_width={value}"

    await ctx.send(f"URL : {url}")
