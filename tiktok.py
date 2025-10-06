from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

@app.get("/tiktok", response_class=HTMLResponse)
def get_tiktok(url: str = Query(...)):
    oembed_url = f"https://www.tiktok.com/oembed?url={url}"
    r = requests.get(oembed_url)
    data = r.json()

    html_content = f"""
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{data.get('author_name')} - TikTok</title>
      </head>
      <body style="display:flex;justify-content:center;align-items:center;height:100vh;background:#000;">
        <div style="max-width:600px;width:100%;">{data['html']}</div>
      </body>
    </html>
    """
    return HTMLResponse(content=html_content)
