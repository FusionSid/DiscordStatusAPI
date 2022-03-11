import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

async def get_user_data(user_id):
    try:
        headers = {'Authorization': f"Bot {os.environ['TOKEN']}"}

        url = f"https://discord.com/api/v8/users/{user_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as data:
                if data.status == 400:
                    return False
                user = await data.json()

        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.png"

        return [
            user, 
            avatar_url
        ]
    except Exception:
        return False