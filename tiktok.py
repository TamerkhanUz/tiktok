from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
import requests

app = FastAPI()

# TikTok videolarini olish uchun oddiy proxy endpoint
@app.get("/tiktok")
def get_tiktok(url: str):
    try:
        # TikTok API orqali oEmbed ma'lumotini olish
        r = requests.get(f"https://www.tiktok.com/oembed?url={url}", timeout=10)
        if r.status_code != 200:
            return JSONResponse({"error": "TikTokdan javob yo‘q"}, status_code=400)
        data = r.json()
        return {
            "author_name": data.get("author_name"),
            "title": data.get("title"),
            "thumbnail_url": data.get("thumbnail_url"),
            "html": data.get("html"),
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# TikTok video faylini to‘g‘ridan-to‘g‘ri oqim orqali olish (CDN proxy)
@app.get("/video")
def stream_video(url: str):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, stream=True)
        return StreamingResponse(r.iter_content(chunk_size=8192), media_type="video/mp4")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
