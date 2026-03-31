# Fraud Ring Early Warning — Deck Outline

1) Title Slide
   - Title: "Fraud Ring Early Warning"
   - Tagline: "Find mule rings by tracing shared devices, IPs, phones, and money flow"
   - Event: Devacation 2026 Powered by TigerGraph
   - Team: CLOUDFORCE
   - Members: Satyam Mall, Akash, Shaurya Srivastava
   - Shaurya role: Presentation

2) Problem Slide
   - Fraud rings reuse the same devices, IPs, and phone numbers across many accounts.
   - Rule-based systems miss multi-hop patterns and are hard to explain to investigators.
   - Result: alerts are noisy, slow to review, and easy to miss.

3) Graph Model Slide
   - Vertices: `Account`, `Device`, `Phone`, `IPAddr`, `Merchant`
   - Edges: `UsesDevice`, `HasPhone`, `AtIP`, `Transfer`, `ShopsAt`
   - Why graph: shared identifiers + transaction paths reveal coordinated behavior quickly.

4) Solution Slide
   - `ringDetect(src, min_shared, top_k)` finds connected accounts sharing assets with a seed account.
   - `muleRanking(top_k)` ranks suspicious accounts by shared activity and network degree.
   - Explainability: each result shows `shared_count`, `deg_in`, `deg_out`, and risk context.

5) Demo Slide
   - Start from one account, like `acct_0000`.
   - Run the live viewer at `docs/index.html` or `ringdetect-view.html`.
   - REST example: `http://localhost:9000/query/Fraud/ringDetect?src=acct_0000&min_shared=2&top_k=10`
   - Screenshot idea: query result table + one JSON response snippet.

6) Impact Slide
   - Detects rings in one query instead of manual graph tracing.
   - Helps analysts prioritize the highest-risk accounts first.
   - Reduces false positives by focusing on relationship patterns, not isolated transactions.

7) Next Steps Slide
   - Add merchant risk signals and time-window filters.
   - Improve scoring with amount thresholds and recent activity.
   - Extend the UI with path visualization and exportable case notes.

8) Team Slide
   - Team: CLOUDFORCE
   - Satyam Mall: data, GSQL, TigerGraph setup
   - Akash: UI, demo flow, submission assets
   - Shaurya Srivastava: presentation
   - Add contact info before submission

Notes for slides
- Keep each slide to 2 to 4 bullets.
- Use one screenshot from the live query and one architecture diagram if possible.
- Keep the story simple: problem -> graph -> query -> demo -> impact.
