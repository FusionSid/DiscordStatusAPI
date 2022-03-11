import os
import asyncio
import discord
from utils import Card
from dotenv import load_dotenv
from discord.ext import commands
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse


load_dotenv()


TOKEN = os.environ["TOKEN"]


client = commands.Bot(">", intents=discord.Intents.all())


app = FastAPI()


@app.get("/api/image")
async def image(request : Request, user_id : int):
    main_guild = await client.fetch_guild(942546789372952637)
    user = await main_guild.fetch_member(user_id)
    
    if user is None:
        return {"error" : "User not in guild or doesn't exist"}

    card = Card(user)

    if user.activity is None:
        image = await card.status_image()
    else:
        image = await card.activity_image()
        
    return StreamingResponse(image, 200, media_type="image/png")


@app.on_event("startup")
async def startup_event():
  asyncio.create_task(client.start(TOKEN))