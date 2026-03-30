# Cloudforce Fraud Ring Demo — Deploy Guide

## Repo name (suggested)
`cloudforce-fraud-ring`

## What’s inside
- `fraud-ring-demo/gsql/` — schema, loading job, queries.
- `fraud-ring-demo/data/` — synthetic CSVs + generator script.
- `fraud-ring-demo/submission/` — proxy (`proxy.py`), HTML viewer, requirements.
- `docs/ringdetect-view.html` — static page for GitHub Pages.

## Local quickstart (TigerGraph already loaded)
```bash
docker start tg
# run proxy (adds CORS + token auth):
cd fraud-ring-demo/submission
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python proxy.py   # serves on http://127.0.0.1:8089
# serve viewer
cd ..
python3 -m http.server 8088   # open http://localhost:8088/docs/ringdetect-view.html
```

## Remote deploy (proxy + Pages)
1) Deploy proxy (Render/Heroku/Railway):
   - `cd fraud-ring-demo/submission`
   - Add env vars: `TG_BASE`, `TG_USER`, `TG_PASSWORD`, `TG_GRAPH` (defaults are in file).
   - Procfile (already implied by gunicorn): `web: gunicorn proxy:app`
2) Static site:
   - GitHub Pages → source: `main` / `docs`.
   - URL: `https://<your-username>.github.io/cloudforce-fraud-ring/ringdetect-view.html`
   - In `docs/ringdetect-view.html` set `const BASE = "https://<your-proxy>/api/ringDetect";`

## TigerGraph reload (if needed)
```bash
# inside container tg as tigergraph user
/home/tigergraph/tigergraph/app/cmd/gsql -u tigergraph -p Hackathon123 "RUN LOADING JOB load_fraud"
```

## Queries (installed)
- `ringDetect(src, min_shared, top_k)` — REST: `/query/Fraud/ringDetect`
- `muleRanking(top_k)` — REST: `/query/Fraud/muleRanking`
