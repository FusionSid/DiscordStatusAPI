import aiohttp
import textwrap
import discord
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps
import os

cwd = os.getcwd()

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
        img = Image.open(f"{cwd}/assets/images/online.png")

    elif status == discord.Status.dnd:
        img = Image.open(f"{cwd}/assets/images/dnd.png")

    elif status == discord.Status.idle:
        img = Image.open(f"{cwd}/assets/images/idle.png")

    elif status == discord.Status.invisible:
        img = Image.open(f"{cwd}/assets/images/offline.png")

    elif status == discord.Status.offline:
        img = Image.open(f"{cwd}/assets/images/offline.png")

    elif status == discord.Status.streaming:
        img = Image.open(f"{cwd}/assets/images/online.png")

    else:
        img = Image.open(f"{cwd}/assets/images/offline.png")
        
    status_img = Image.new("RGBA", (50, 50), (255, 255, 255, 0))
    
    img = img.resize((40, 40))
    status_img.paste(img, (3, 3))

    # Draw border
    draw = ImageDraw.Draw(status_img)
    north_west = (0, 0)
    south_east = (45, 45)
    draw.ellipse([north_west, south_east], outline="#161a1d", width=5)

    return status_img

class Card():
    def __init__(self, member):
        self.id = member.id
        self.name = member.name # max length = 30 if your name is longer, first of all why and second too bad
        self.status = member.status
        self.activity = member.activity
        self.avatar_url = member.avatar.url
        self.discriminator = member.discriminator
    

    async def status_image(self):
        # Generate Image
        discord_image = Image.new("RGBA", (450, 170), "#161a1d")
    
        # Fonts
        font_1 = ImageFont.truetype("assets/fonts/uni_sans_heavy.otf", 20)
        font_2 = ImageFont.truetype("assets/fonts/whitneybold.otf", 50)

        font_3 = ImageFont.truetype("assets/fonts/whitneylight.otf", 40)

        # Avatar
        avatar = await get_avatar(self.avatar_url)
        discord_image.alpha_composite(avatar, (25, 25))


        # Status
        status = await get_status(self.status)
        discord_image.alpha_composite(status, (105, 110))

        # Draw text
        draw = ImageDraw.Draw(discord_image)

        # draw name
        if len(self.name) <= 10:
            draw.text((180,35), self.name, fill="white", font=font_2, align='left')
        else:
            font_2 = ImageFont.truetype("assets/fonts/whitneybold.otf", 30)
            w, h = 590, 30 
            lines = textwrap.wrap(self.name, width=15)
            y_text = h
            for line in lines:
                width, height = font_2.getsize(line)
                draw.text(((w - width) / 2, y_text), line, font=font_2, fill="white", align="left")
                y_text += height 
        

        # draw discriminator
        draw.text((180, 90), f"#{self.discriminator}", fill="white", font=font_3, align='left')

        # Save and return
        final_image = BytesIO()
        final_image.seek(0)
        discord_image.save(final_image, "PNG")
        final_image.seek(0)

        return final_image


    async def activity_image(self):
        pass