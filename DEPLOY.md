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
   - Add env vars to match Savanna:
     - `TG_BASE=https://tg-3b54a662-9c06-49cb-ad2a-25939dfb441c.tg-2635877100.i.tgcloud.io/restpp`
     - `TG_GRAPH=Fraud`
     - `TG_TOKEN=<paste token returned by requesttoken>` (preferred) or `TG_USER`/`TG_PASSWORD`
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

> **Token status:** Authorization requests to `/restpp/requesttoken` have been returning HTTP 400 for now. Keep the proxy running locally (it uses cloud REST++ via `TG_BASE` with no token) and document in the submission form that a Savanna token is pending; the same request above will work instantly once the secret is accepted.

## TigerGraph reload (if needed)
```bash
# inside container tg as tigergraph user
/home/tigergraph/tigergraph/app/cmd/gsql -u tigergraph -p Hackathon123 "RUN LOADING JOB load_fraud"
```

## Queries (installed)
- `ringDetect(src, min_shared, top_k)` — REST: `/query/Fraud/ringDetect`
- `muleRanking(top_k)` — REST: `/query/Fraud/muleRanking`
