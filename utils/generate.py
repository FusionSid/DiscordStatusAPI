from PIL import Image, ImageDraw, ImageFilter, ImageFont
from io import BytesIO


async def generate_discord_image(member):
    return "Not made yet lol"

    activity = member.activity
    status = member.status

    # Fonts
    font_1 = ImageFont.truetype("assets/fonts/uni_sans_heavy.otf", 20)


    # Background
    image_background = Image.open("assets/images/background.png")
    image_background = image_background.convert("RGB")
    image_background = image_background.filter(ImageFilter.GaussianBlur(radius=5))

    # Generate Image
    discord_image = Image.new("RGB", (450, 170), "black")
    discord_image.paste(image_background, (0, 0))

    # Draw text
    draw = ImageDraw.Draw(discord_image)

    if activity != "None":
        pass
    else:
        pass


    # Save and return
    final_image = BytesIO()
    final_image.seek(0)
    discord_image.save(final_image, "PNG")
    final_image.seek(0)

    return final_image


class Card():
    def __init__(self, member):
        self.id = member.id
        self.name = member.name
        self.status = member.status
        self.activity = member.activity
        self.discriminator = member.discriminator

    
    async def status_image(self):
        # Fonts
        font_1 = ImageFont.truetype("assets/fonts/uni_sans_heavy.otf", 20)
        font_2 = None

        # # Background
        # image_background = Image.open("assets/images/background.png")
        # image_background = image_background.convert("RGB")
        # image_background = image_background.filter(ImageFilter.GaussianBlur(radius=5))

        # Generate Image
        discord_image = Image.new("RGB", (450, 170), "161a1d")
        # discord_image.paste(image_background, (0, 0))

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

        # # Background
        # image_background = Image.open("assets/images/background.png")
        # image_background = image_background.convert("RGB")
        # image_background = image_background.filter(ImageFilter.GaussianBlur(radius=5))

        # Generate Image
        discord_image = Image.new("RGB", (450, 170), "161a1d")
        # discord_image.paste(image_background, (0, 0))

        # Draw text
        draw = ImageDraw.Draw(discord_image)

        # Save and return
        final_image = BytesIO()
        final_image.seek(0)
        discord_image.save(final_image, "PNG")
        final_image.seek(0)

        return final_image