# Cloudforce Fraud Ring

TigerGraph-powered fraud-ring early warning demo for Devacation 2026.

Live preview: https://satyamhub.github.io/cloudforce-fraud-ring/

We built a graph-native fraud detector that turns one suspicious account into a full investigation path in seconds.
The graph reveals shared devices, phones, IPs, merchants, and money-flow links that fraud rings use to hide in plain sight.

> One suspicious account. One graph query. The full ring.

- Event: Devacation 2026 Powered by TigerGraph
- Team: CLOUDFORCE
- Focus: Fraud ring early warning and explainable graph analytics

## Quick Links

- Preview: https://satyamhub.github.io/cloudforce-fraud-ring/
- Deck PDF: `CLOUDFORCE_Fraud_Ring_Early_Warning.pdf`
- Deploy guide: `DEPLOY.md`
- Interactive viewer: `docs/ringdetect-view.html`

## About

Cloudforce Fraud Ring is a TigerGraph-powered fraud detection demo that surfaces coordinated mule rings by tracing shared devices, phones, IPs, merchants, and money-flow paths.
The system starts from one suspicious account, expands the connected network, and explains why each suspect looks risky so investigators can move fast.

## What It Does

- `ringDetect(src, min_shared, top_k)` expands from one account to the connected suspicious ring.
- `muleRanking(top_k)` ranks suspicious accounts using shared activity and network signals.
- A secure Flask proxy keeps TigerGraph secrets off the browser.
- A polished HTML viewer makes the demo judge-friendly and easy to understand.

## Architecture

`Data -> TigerGraph graph + queries -> secure proxy -> HTML viewer -> judge-friendly demo`

## Why This Stands Out

- Real-world fraud rings often reuse the same device, IP, phone, or merchant across many accounts.
- Graph analytics exposes the hidden pattern that regular transaction rules miss.
- The UI is built for presentation: simple inputs, explainable results, and clear story flow.
- The repo includes both the code and the submission-ready deck assets.

## Live Demo

- Preview: https://satyamhub.github.io/cloudforce-fraud-ring/
- Presentation page: `docs/index.html`
- Interactive viewer: `docs/ringdetect-view.html`
- Deploy guide: `DEPLOY.md`

## Screenshots

- Presentation UI: `docs/index.html`
- Interactive ringDetect viewer: `docs/ringdetect-view.html`

## Project Structure

- `fraud-ring-demo/gsql/` - graph schema, loading job, and queries
- `fraud-ring-demo/data/` - synthetic fraud-ring dataset generator and CSVs
- `fraud-ring-demo/submission/` - proxy, viewer, and submission notes
- `docs/` - GitHub Pages-ready landing page and viewer
- `assets/` - TigerGraph branding used in the deck

## Decks

- `CLOUDFORCE_Fraud_Ring_Early_Warning.pptx`
- `CLOUDFORCE_Fraud_Ring_Early_Warning_short.pptx`
- `CLOUDFORCE_Fraud_Ring_Early_Warning_screenshots.pptx`
- `CLOUDFORCE_Fraud_Ring_Early_Warning.pdf`

## Quick Start

1. Generate the sample data:
   ```bash
   cd fraud-ring-demo
   python3 data/generate_data.py
   ```
2. Load the graph and queries into TigerGraph.
3. Run the proxy from `fraud-ring-demo/submission/proxy.py`.
4. Open `docs/index.html` or `docs/ringdetect-view.html`.

## Why It Matters

Fraud rings are hard to detect when each transaction is viewed alone. Graph analytics makes the connection pattern visible, helping investigators explain why an account is suspicious and prioritize the riskiest cases first.

## Presentation Hook

> "Fraud rings hide by reusing the same devices, IPs, phones, and merchants across many accounts. Cloudforce exposes that hidden network with TigerGraph."

## Team

- Satyam Mall
- Akash
- Shaurya Srivastava

## Hackathon

- Event: Devacation 2026 Powered by TigerGraph
- Team: CLOUDFORCE
