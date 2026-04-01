# Cloudforce Fraud Ring

Detect coordinated fraud rings with a graph-native investigation flow built on TigerGraph.

![TigerGraph logo](assets/tigergraph-logo.png)

Live preview: https://cloudforce.vercel.app/
Static preview: https://satyamhub.github.io/cloudforce-fraud-ring/

Cloudforce turns one suspicious account into a full investigation path in seconds.
It exposes shared devices, phones, IPs, merchants, and money-flow links that fraud rings use to hide in plain sight.

> One suspicious account. One graph query. The full ring.

- Event: Devacation 2026 Powered by TigerGraph
- Team: CLOUDFORCE
- Focus: Fraud ring early warning and explainable graph analytics

## Quick Links

- Deck PDF: `CLOUDFORCE_Fraud_Ring_Early_Warning.pdf`
- Interactive viewer: `docs/ringdetect-view.html`
- Submission video: `fraud-ring-demo/submission/Cloudforce_Fraud_Ring_Demo_Male_Short.mp4`

## About

Cloudforce Fraud Ring is a TigerGraph-powered fraud detection demo for coordinated mule rings.
It starts from one suspicious account, expands the connected network, and explains why each suspect looks risky so investigators can move fast.

## What It Does

- `ringDetect(src, min_shared, top_k)` expands one account into the connected suspicious ring.
- `muleRanking(top_k)` ranks suspicious accounts with shared activity and network signals.
- A lightweight Flask proxy keeps the demo tokenless by default, with optional cloud auth later.
- A polished HTML viewer keeps the demo judge-friendly and easy to follow.

## Architecture

Data flows from TigerGraph queries through a tokenless proxy into a judge-friendly HTML viewer.

## Why This Stands Out

- Real-world fraud rings often reuse the same device, IP, phone, or merchant across many accounts.
- Graph analytics exposes the hidden pattern that regular transaction rules miss.
- The UI is built for presentation: simple inputs, explainable results, and a clear story flow.
- The repo includes the code and submission deck assets.

## Live Demo

- Presentation page: `docs/index.html`
- Interactive viewer: `docs/ringdetect-view.html`

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

## Submission

The submission package centers on the demo video and web viewer:

- Demo video: `fraud-ring-demo/submission/Cloudforce_Fraud_Ring_Demo_Male_Short.mp4`
- Interactive viewer: `docs/ringdetect-view.html`
- Presentation page: `docs/index.html`

## Quick Start

1. Generate the sample data:
   ```bash
   cd fraud-ring-demo
   python3 data/generate_data.py
   ```
2. Load the graph and queries into TigerGraph.
3. Run the proxy from `fraud-ring-demo/submission/proxy.py`.
4. Open the presentation page or interactive viewer.

## Why It Matters

Fraud rings are hard to detect when each transaction is viewed alone. Graph analytics makes the connection pattern visible, helping investigators explain why an account is suspicious and prioritize the riskiest cases first.

## Presentation Hook

> Fraud rings hide by reusing the same devices, IPs, phones, and merchants across many accounts. Cloudforce exposes that hidden network with TigerGraph.

## Team

- Satyam Mall
- Akash
- Shaurya Srivastava

## Hackathon

- Event: Devacation 2026 Powered by TigerGraph
- Team: CLOUDFORCE
