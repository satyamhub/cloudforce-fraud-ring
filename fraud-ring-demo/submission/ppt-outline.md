# Fraud Ring Early Warning — Deck Outline

1) Title
   - "Fraud Ring Early Warning" (TigerGraph)
   - Team: CLOUDFORCE — Satyam Mall, Akash

2) Problem
   - Fraud rings reuse devices/IPs/phones to mule money across accounts.
   - Need fast, explainable detection; existing rule engines miss multi-hop patterns.

3) Data Model (Graph)
   - Vertices: Account(pid, flagged), Device, Phone, IPAddr, Merchant
   - Edges: UsesDevice, HasPhone, AtIP, Transfer(Account→Account), ShopsAt(Account→Merchant)
   - Why: shared-asset links + money flow let us spot rings and rank mules.

4) Queries
   - ringDetect(src, min_shared, top_k): find accounts sharing assets with src; rank by shared_count + in/out degree.
   - muleRanking(top_k): rank accounts by (distinct devices × IPs) adjusted for account age.
   - REST++ endpoints (ready):
     - ringDetect: `http://localhost:9000/query/Fraud/ringDetect?src=acct_0000&min_shared=2&top_k=10`
     - muleRanking: `http://localhost:9000/query/Fraud/muleRanking?top_k=10`

5) Demo Evidence (from current run)
   - ringDetect("acct_0000",2,10) returns 7 suspects (top: acct_0001, shared_count=5, deg_out=10, deg_in=9).
   - Screenshot idea: REST JSON snippet + GraphStudio table filtered on ringDetect output.

6) Impact & Metrics
   - Surfaces a ring of 7 accounts around a single seed in one query.
   - Prioritize suspects by shared_count and money-flow degree to cut alert noise.
   - Future metric: alert precision/recall vs. baseline rules (to be measured on labeled set).

7) Next Steps
   - Add merchant risk signals (flagged merchants) into scoring.
   - Add time-window filters (last 7/30 days) and amount thresholds.
   - Simple UI: table + path view for explainability; export CSV for investigators.

8) Team & Roles
   - CLOUDFORCE
     - Satyam Mall — data & GSQL queries; TigerGraph ops
     - Akash — UI/demo & submission assets
   - Add contact: email / phone / GitHub (fill before submission)

Notes for slides
- Use 1–2 bullets per box; include the REST URL and one JSON screenshot for credibility.
- Keep color-coding: shared assets vs. money flow.
