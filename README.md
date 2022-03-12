![](https://discordimage.herokuapp.com/api/image?user_id=624076054969188363&rounded_corners=true&resize_width=150)

# Discord Image API

### Join the [DISCORD SERVER](https://discord.com/invite/p9GuT5hakm) For it to work
The [why discord server](https://discord.gg/Jm8QPF6xbN) will work too

**[DOCS](https://discordimage.herokuapp.com/docs)** 

---

## Usage:

**URL:** `https://discordimage.herokuapp.com/api/image?user_id=[Your discord id]`

---

## Example:

### URL:
https://discordimage.herokuapp.com/api/image?user_id=624076054969188363


### Result:

This is a live example of this, this image will update if I go offline
[![Example Image](https://discordimage.herokuapp.com/api/image/?user_id=624076054969188363)](https://discordimage.herokuapp.com/docs)

Other Parameters: 

`&rounded_corners=False` to the end of the url for them to not be rounded

- If this is not included in url it defaults to true

`&resize_width=[custom_width]` resizes to that width (example the mini one at the top of the readme)

- This does reduce image quality though
- Also max width = 4269 

### How it works
This api runs a discord bot at the same time in the same file, whenever you make a request the bot just looks at what your presence is and returns it back to the api which then makes an image and returns it
