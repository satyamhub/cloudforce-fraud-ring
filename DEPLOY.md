# Cloudforce Fraud Ring Demo — Deploy Guide

## Repo name
`cloudforce-fraud-ring`

## Public preview
- `https://cloudforce.vercel.app/`
- Public API: `https://cloudforce.vercel.app/api/ringDetect`

## What’s inside
- `fraud-ring-demo/gsql/` — schema, loading job, queries.
- `fraud-ring-demo/data/` — synthetic CSVs + generator script.
- `fraud-ring-demo/submission/` — proxy (`proxy.py`), HTML viewer, requirements.
- `docs/ringdetect-view.html` — static page for GitHub Pages.

## Local quickstart (TigerGraph already loaded)
```bash
docker start tg
# run proxy against the local TigerGraph instance:
cd fraud-ring-demo/submission
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python proxy.py   # serves on http://127.0.0.1:8089
# serve viewer
cd ..
python3 -m http.server 8088   # open http://localhost:8088/docs/ringdetect-view.html
```
The local proxy defaults to `TG_BASE=http://localhost:9000`, so no Savanna token is needed for the demo once the TigerGraph container is running.
The public Vercel preview serves the same pages and uses the bundled CSV-backed `/api/ringDetect` endpoint.

## Remote deploy (proxy + Pages)
1) Deploy proxy (Render/Heroku/Railway):
   - `cd fraud-ring-demo/submission`
   - Add env vars to match Savanna:
     - `TG_BASE=https://tg-3b54a662-9c06-49cb-ad2a-25939dfb441c.tg-2635877100.i.tgcloud.io/restpp`
     - `TG_GRAPH=Fraud`
     - `TG_TOKEN=<paste token returned by requesttoken>` if you are using the cloud workspace
   - Procfile (already implied by gunicorn): `web: gunicorn proxy:app`
   - Token request example (use `secret` from Admin Portal):
     ```bash
     curl -k -X POST "https://<host>/requesttoken" \
       -H "Content-Type: application/json" \
       -d '{"secret":"<value>","graph":"Fraud","lifetime":3600}'
     ```
2) Static site:
   - GitHub Pages → source: `main` / `docs`.
   - URL: `https://<your-username>.github.io/cloudforce-fraud-ring/ringdetect-view.html`
   - In `docs/ringdetect-view.html` set `const BASE = "https://<your-proxy>/api/ringDetect";`

> **Token status:** The local demo path does not require a Savanna token. If you deploy the proxy to the cloud, add `TG_TOKEN` there; otherwise the default local setup uses `http://localhost:9000` and works without auth.

## TigerGraph reload (if needed)
```bash
# inside container tg as tigergraph user
/home/tigergraph/tigergraph/app/cmd/gsql -u tigergraph -p Hackathon123 "RUN LOADING JOB load_fraud"
```

## Queries (installed)
- `ringDetect(src, min_shared, top_k)` — REST: `/query/Fraud/ringDetect`
- `muleRanking(top_k)` — REST: `/query/Fraud/muleRanking`
