from fastapi import FastAPI, Request
import uvicorn
from threading import Thread
from utils import generate_discord_image, generate_discord_json
from fastapi.responses import StreamingResponse, FileResponse


app = FastAPI()

@app.get("/image")
async def image(request : Request, user_id : int):
    image = await generate_discord_image(user_id)
    if type(image) == str:
        return {"error" : image}
        
    return StreamingResponse(image, 200, media_type="image/png")


@app.get("/json")
async def json_discord(request : Request, user_id : int):
    json_resp = await generate_discord_json(user_id)
    if type(image) == str:
        return {"error" : image}

    return json_resp
    
def run():
    uvicorn.run(app)

def run_api():
    t = Thread(target=run)
    t.daemon = True
    t.start()