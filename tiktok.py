# fayl nomi: app.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
import requests
from urllib.parse import urlparse

app = FastAPI()

@app.get("/tiktok")
def tiktok(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        return HTMLResponse(content=resp.text)
    except Exception as e:
        return JSONResponse({"error": str(e)})

@app.get("/fetch")
def fetch(url: str):
    """TikTok ichki resurslari (JS, CSS, video) uchun proxy"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        content_type = r.headers.get("content-type", "text/html")
        return Response(content=r.content, media_type=content_type)
    except Exception as e:
        return JSONResponse({"error": str(e)})
