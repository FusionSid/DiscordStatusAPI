import aiohttp
import discord
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops

async def get_avatar(avatar_url):
    async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as resp:
                avatar_data = await resp.read()

    im = Image.open(BytesIO(avatar_data)).resize((125, 125))
    im = im.convert("RGBA")

    background = Image.new("RGBA", size=im.size, color=(255, 255, 255, 0))
    holder = Image.new("RGBA", size=im.size, color=(255, 255, 255, 0))
    mask = Image.new("RGBA", size=im.size, color=(255, 255, 255, 0))
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0) + im.size, fill="black")
    holder.paste(im, (0, 0))
    img = Image.composite(holder, background, mask)

    return img


async def get_status(status):
    if status == discord.Status.online:
        img = Image.open("assets/images/online.png")
    else:
        img = Image.open("assets/images/online.png")

    img = img.resize((40, 40))
    return img

class Card():
    def __init__(self, member):
        self.id = member.id
        self.name = member.name
        self.status = member.status
        self.activity = member.activity
        self.avatar_url = member.avatar.url
        self.discriminator = member.discriminator
    
    async def status_image(self):
        # Generate Image
        discord_image = Image.new("RGBA", (450, 170), "#161a1d")
    
        # Fonts
        font_1 = ImageFont.truetype("assets/fonts/uni_sans_heavy.otf", 20)
        font_2 = None

        # Avatar
        avatar = await get_avatar(self.avatar_url)
        discord_image.alpha_composite(avatar, (25, 25))


        # Status
        status = await get_status(self.status)
        discord_image.alpha_composite(status, (110, 110))

        # Draw text
        draw = ImageDraw.Draw(discord_image)

        # Save and return
        final_image = BytesIO()
        final_image.seek(0)
        discord_image.save(final_image, "PNG")
        final_image.seek(0)

        return final_image


    async def activity_image(self):
        # Fonts
        font_1 = ImageFont.truetype("assets/fonts/uni_sans_heavy.otf", 20)
        font_2 = None

        # Generate Image
        discord_image = Image.new("RGB", (450, 170), "161a1d")

        # Draw text
        draw = ImageDraw.Draw(discord_image)

        # Save and return
        final_image = BytesIO()
        final_image.seek(0)
        discord_image.save(final_image, "PNG")
        final_image.seek(0)

        return final_image