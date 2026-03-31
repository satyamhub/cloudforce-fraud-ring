"""
Lightweight CORS proxy for TigerGraph REST++.

Usage:
  python3 -m pip install flask requests
  python3 proxy.py   # starts on http://localhost:8089

Then point the HTML viewer at: http://localhost:8089/api/ringDetect
"""

from flask import Flask, request, Response
import os
import csv
import json
from collections import defaultdict, Counter
from pathlib import Path
import requests

TG_BASE = os.getenv(
    "TG_BASE",
    "http://localhost:9000",
)
TG_GRAPH = os.getenv("TG_GRAPH", "Fraud")
TG_TOKEN_OVERRIDE = os.getenv("TG_TOKEN")
DATA_DIR = Path(__file__).resolve().parents[1] / "data"

_ACCOUNT_META = {}
_ACCOUNT_DEVICES = defaultdict(set)
_ACCOUNT_IPS = defaultdict(set)
_ACCOUNT_PHONES = defaultdict(set)
_OUT_DEG = Counter()
_IN_DEG = Counter()


def _load_local_data():
    accounts_path = DATA_DIR / "accounts.csv"
    account_device_path = DATA_DIR / "account_device.csv"
    account_ip_path = DATA_DIR / "account_ip.csv"
    account_phone_path = DATA_DIR / "account_phone.csv"
    transfers_path = DATA_DIR / "transfers.csv"

    if not accounts_path.exists():
        return

    with accounts_path.open(newline="") as f:
        for row in csv.reader(f):
            if len(row) < 4:
                continue
            pid, flagged, _created_at, risk_score = row[:4]
            _ACCOUNT_META[pid] = {
                "pid": pid,
                "flagged": int(flagged),
                "risk_score": float(risk_score),
            }

    for path, target in [
        (account_device_path, _ACCOUNT_DEVICES),
        (account_ip_path, _ACCOUNT_IPS),
        (account_phone_path, _ACCOUNT_PHONES),
    ]:
        if not path.exists():
            continue
        with path.open(newline="") as f:
            for row in csv.reader(f):
                if len(row) < 2:
                    continue
                acct, value = row[:2]
                target[acct].add(value)

    if transfers_path.exists():
        with transfers_path.open(newline="") as f:
            for row in csv.reader(f):
                if len(row) < 2:
                    continue
                src, dst = row[:2]
                _OUT_DEG[src] += 1
                _IN_DEG[dst] += 1


_load_local_data()

app = Flask(__name__)

def forward(path):
    url = f"{TG_BASE}{path}"
    headers = {}
    if TG_TOKEN_OVERRIDE:
        headers["Authorization"] = f"Bearer {TG_TOKEN_OVERRIDE}"
    try:
        r = requests.get(url, params=request.args, headers=headers, timeout=15)
        resp = Response(
            r.content,
            status=r.status_code,
            content_type=r.headers.get("Content-Type", "application/json"),
        )
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
    except requests.RequestException:
        if TG_BASE.startswith("http://localhost:9000"):
            return _local_ring_detect()
        raise


def _local_ring_detect():
    src = request.args.get("src", "").strip()
    min_shared = int(request.args.get("min_shared", 2))
    top_k = int(request.args.get("top_k", 10))

    if src not in _ACCOUNT_META:
        payload = {"results": [{"ordered": []}]}
        resp = Response(json.dumps(payload), status=200, content_type="application/json")
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp

    src_assets = (
        _ACCOUNT_DEVICES.get(src, set()),
        _ACCOUNT_PHONES.get(src, set()),
        _ACCOUNT_IPS.get(src, set()),
    )
    src_devices, src_phones, src_ips = src_assets

    rows = []
    for acct, meta in _ACCOUNT_META.items():
        if acct == src:
            continue
        shared_count = (
            len(src_devices & _ACCOUNT_DEVICES.get(acct, set()))
            + len(src_phones & _ACCOUNT_PHONES.get(acct, set()))
            + len(src_ips & _ACCOUNT_IPS.get(acct, set()))
        )
        if shared_count < min_shared:
            continue
        rows.append(
            {
                "attributes": {
                    "pid": meta["pid"],
                    "flagged": meta["flagged"],
                    "risk_score": meta["risk_score"],
                    "@shared_count": shared_count,
                    "@deg_out": _OUT_DEG.get(acct, 0),
                    "@deg_in": _IN_DEG.get(acct, 0),
                }
            }
        )

    rows.sort(
        key=lambda r: (
            -r["attributes"]["@shared_count"],
            -r["attributes"]["@deg_out"],
            -r["attributes"]["@deg_in"],
            r["attributes"]["pid"],
        )
    )
    payload = {"results": [{"ordered": rows[:top_k]}]}
    resp = Response(json.dumps(payload), status=200, content_type="application/json")
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.route("/api/ringDetect")
def ring_detect():
    return forward(f"/query/{TG_GRAPH}/ringDetect")


if __name__ == "__main__":
    app.run(port=8089)
