![](https://discordimage.herokuapp.com/api/image?user_id=624076054969188363&rounded_corners=true&show_activity=true&resize_width=150&name_color=%235a189a&discriminator_color=%237b2cbf&activity_color=white&background_color=%2310002b)

# Discord Image API

**[API DOCS](https://discordimage.herokuapp.com/docs)** 

### Join the [DISCORD SERVER](https://discord.com/invite/p9GuT5hakm) For it to work
The [why discord server](https://discord.gg/Jm8QPF6xbN) will work too

---

## Usage:

**URL:** `https://discordimage.herokuapp.com/api/image?user_id=[Your discord id]`

## Extra Parameters: 

`&rounded_corners=[True/False]]` sets if the corners should be rounded or not

- If this is not included in url it defaults to true

`&resize_width=[custom_width]` resizes to that width (example the mini one at the top of the readme)

- This does reduce image quality though
- Also max width = 4269 

`&name_color=[color]` Changes the color for the **name** text

- defaults to **white**
- supports colors by name like "white", "blue", "purple" etc 
- supports hex colors like "#FFFFFF"
- if color is invalid it will go back to default

`&discriminator_color=[color]` Changes the color for the **name** text

- defaults to **#161a1d**
- supports colors by name like "white", "blue", "purple" etc 
- supports hex colors like "#FFFFFF"
- if color is invalid it will go back to default

`&background_color=[color]` Changes the color for the **background** text

- defaults to **white**
- supports colors by name like "white", "blue", "purple" etc 
- supports hex colors like "#FFFFFF"
- if color is invalid it will go back to default

`&show_activity=[True/False]]` Show activity or not
- By default if the api sees that you are playing something it will add that to the bottom of the card

`&activity_color=[color]` Changes the color for the **activity** text

- defaults to **white**
- supports colors by name like "white", "blue", "purple" etc 
- supports hex colors like "#FFFFFF"
- if color is invalid it will go back to default

---

## Example:

### URL:
https://discordimage.herokuapp.com/api/image?user_id=624076054969188363


### Result:

This is a live example of this, this image will update if I am offline, idle, do_not_disturb, invisible or online

[![Example Image](https://discordimage.herokuapp.com/api/image/?user_id=624076054969188363)](https://discordimage.herokuapp.com/docs)

### How it works
This api runs a discord bot at the same time in the same file, whenever you make a request the bot just looks at what your presence is and returns it back to the api which then makes an image and returns it
