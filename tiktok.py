import requests
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/tiktok")
def proxy_tiktok(url: str = Query(...)):
    proxies = {
        "http": "http://38.242.228.144:8081",
        "https": "http://38.242.228.144:8081",
    }
    try:
        resp = requests.get(url, proxies=proxies, timeout=10)
        return {"status": resp.status_code, "headers": dict(resp.headers)}
    except Exception as e:
        return {"error": str(e)}
