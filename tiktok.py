# Fayl: tiktok_proxy.py
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, StreamingResponse, Response
import requests, urllib.parse, re

app = FastAPI()
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Referer": "https://www.tiktok.com/", "Accept-Language": "en-US,en;q=0.9"}

# -------------- Helper --------------
def proxy_get(url, stream=False, headers=None, timeout=20):
    h = HEADERS.copy()
    if headers:
        h.update(headers)
    return requests.get(url, headers=h, stream=stream, timeout=timeout)

# -------------- Endpoints --------------
@app.get("/tiktok", response_class=HTMLResponse)
def tiktok_embed(url: str = Query(...)):
    """Return an HTML page with TikTok embed (oembed) whose embed.js is rewritten to /embed.js"""
    oembed_url = f"https://www.tiktok.com/oembed?url={urllib.parse.quote_plus(url)}"
    r = proxy_get(oembed_url, stream=False)
    if r.status_code != 200:
        return HTMLResponse(f"<h3>Error fetching oEmbed: {r.status_code}</h3>", status_code=502)
    data = r.json()
    embed_html = data.get("html", "")
    # Replace the external embed.js with our local endpoint
    embed_html = re.sub(r"<script[^>]*src=[\"']https://www.tiktok.com/embed.js[\"'][^>]*></script>",
                        '<script async src="/embed.js"></script>',
                        embed_html)
    page = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{data.get('author_name','TikTok')}</title>
<style>html,body{{height:100%;margin:0;background:#000;color:#fff;}}</style>
</head>
<body>
  <div id="container" style="height:100vh;display:flex;align-items:center;justify-content:center;">
    <div style="max-width:700px;width:100%;">{embed_html}</div>
  </div>
</body>
</html>"""
    return HTMLResponse(page)

@app.get("/embed.js")
def embed_js():
    """Fetch real embed.js and rewrite resource URLs to go through /fetch?url=..."""
    r = proxy_get("https://www.tiktok.com/embed.js")
    if r.status_code != 200:
        return Response("// failed to fetch embed.js", media_type="application/javascript", status_code=502)
    js = r.text
    # Rewrite "https://..." occurrences to '/fetch?url=https://...'
    # Note: this is a broad rewrite — generally works for resource URLs in embed.js
    def repl(m):
        url = m.group(0)
        return f'"/fetch?url={urllib.parse.quote_plus(url)}"'
    # Replace quoted https urls: "https://... or 'https://...
    js = re.sub(r'["\']https://[^"\']+["\']', repl, js)
    return Response(js, media_type="application/javascript")

@app.get("/fetch")
def fetch_url(url: str = Query(...)):
    """General proxy: fetch any resource and return its bytes (stream for media)."""
    # decode if encoded
    real_url = urllib.parse.unquote_plus(url)
    try:
        r = proxy_get(real_url, stream=True, timeout=30)
    except Exception as e:
        return Response(f"Error fetching: {e}", status_code=502)
    # Try to get content-type
    ctype = r.headers.get("Content-Type", "application/octet-stream")
    # Stream large responses
    return StreamingResponse(r.iter_content(chunk_size=8192), media_type=ctype)

# Optional: direct video-proxy alias
@app.get("/video-proxy")
def video_proxy(url: str = Query(...)):
    return fetch_url(url=url)
