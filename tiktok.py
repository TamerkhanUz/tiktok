import requests
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/tiktok")
def tiktok_proxy(url: str = Query(...)):
    proxies = {
        "http": "http://USERNAME:PASSWORD@PROXY_IP:PORT",
        "https": "http://USERNAME:PASSWORD@PROXY_IP:PORT",
    }
    try:
        resp = requests.get(url, proxies=proxies, timeout=10)
        return {"status": resp.status_code, "headers": dict(resp.headers)}
    except Exception as e:
        return {"error": str(e)}
