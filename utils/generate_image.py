from PIL import Image, ImageDraw, ImageFilter, ImageFont
from io import BytesIO

from .get_user import get_user_data
from .db import get_db_user


async def generate_discord_image(user_id : int):
    
    # Check if exists
    user_data = await get_user_data(user_id)

    if user_data == False:
        return "USER NOT EXISTS"

    user_db_data = await get_db_user(user_id)
    
    if user_db_data == False:
        return "USER NOT IN SERVER"

    # DB Vars

    activity = user_db_data[2]
    status = user_db_data[3]

    if activity == "None" and status == "None":
        return "TRY CHANGING YOUR PRESENCE"

    # Fonts
    font_1 = ImageFont.truetype("assets/fonts/uni_sans_heavy_italic.otf", 20)
    font_2 = ImageFont.truetype("assets/fonts/uni_sans_heavy.otf", 20)
    font_3 = ImageFont.truetype("assets/fonts/uni_sans_thin_italic.otf", 20)
    font_4 = ImageFont.truetype("assets/fonts/uni_sans_thin.otf", 20)

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
    
async def generate_discord_json(user_id : int):
    
    # Check if exists
    user_data = await get_user_data(user_id)

    if user_data == False:
        return "USER NOT EXISTS"

    user_db_data = await get_db_user(user_id)
    
    if user_db_data == False:
        return "USER NOT IN SERVER"

    # DB Vars

    activity = user_db_data[2]
    status = user_db_data[3]

    if activity == "None" and status == "None":
        return "TRY CHANGING YOUR PRESENCE"


    return {
        "user_id" : user_db_data[1],
        "status" : user_db_data[3],
        "activity" : user_db_data[2],
        "name" : user_data[0],
        "avatar_url" : user_data[1]
    }