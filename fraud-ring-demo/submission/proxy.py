"""
Lightweight CORS proxy for TigerGraph REST++.

Usage:
  python3 -m pip install flask requests
  python3 proxy.py   # starts on http://localhost:8089

Then point the HTML viewer at: http://localhost:8089/api/ringDetect
"""

from flask import Flask, request, Response
import requests
import time

TG_BASE = "http://localhost:9000"  # REST++ base
USER = "tigergraph"
PWD = "Hackathon123"
GRAPH = "Fraud"

app = Flask(__name__)

token_cache = {"token": None, "exp": 0}


def get_token():
    now = time.time()
    if token_cache["token"] and now < token_cache["exp"] - 30:
        return token_cache["token"]
    url = f"{TG_BASE}/requesttoken"
    r = requests.post(url, data={"graph": GRAPH, "username": USER, "password": PWD}, timeout=10)
    r.raise_for_status()
    data = r.json()
    token_cache["token"] = data["token"]
    token_cache["exp"] = now + data.get("expiration", 3600)
    return token_cache["token"]


def forward(path):
    token = get_token()
    url = f"{TG_BASE}{path}"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, params=request.args, headers=headers, timeout=15)
    resp = Response(
        r.content,
        status=r.status_code,
        content_type=r.headers.get("Content-Type", "application/json"),
    )
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.route("/api/ringDetect")
def ring_detect():
    return forward(f"/query/{GRAPH}/ringDetect")


if __name__ == "__main__":
    app.run(port=8089)
