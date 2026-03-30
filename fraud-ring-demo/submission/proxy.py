"""
Lightweight CORS proxy for TigerGraph REST++.

Usage:
  python3 -m pip install flask requests
  python3 proxy.py   # starts on http://localhost:8089

Then point the HTML viewer at: http://localhost:8089/api/ringDetect
"""

from flask import Flask, request, Response
import os
import requests
import time

TG_BASE = os.getenv(
    "TG_BASE",
    "https://tg-3b54a662-9c06-49cb-ad2a-25939dfb441c.tg-2635877100.i.tgcloud.io/restpp",
)
TG_GRAPH = os.getenv("TG_GRAPH", "Fraud")
TG_USER = os.getenv("TG_USER", "tigergraph")
TG_PASSWORD = os.getenv("TG_PASSWORD", "Hackathon123")
TG_TOKEN_OVERRIDE = os.getenv("TG_TOKEN")

app = Flask(__name__)

token_cache = {"token": None, "exp": 0}


def get_token():
    if TG_TOKEN_OVERRIDE:
        return TG_TOKEN_OVERRIDE
    now = time.time()
    if token_cache["token"] and now < token_cache["exp"] - 30:
        return token_cache["token"]
    url = f"{TG_BASE}/requesttoken"
    payload = {
        "graph": TG_GRAPH,
        "username": TG_USER,
        "password": TG_PASSWORD,
    }
    r = requests.post(url, json=payload, timeout=10)
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
