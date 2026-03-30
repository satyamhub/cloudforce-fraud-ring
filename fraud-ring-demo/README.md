Fraud Ring Early Warning (TigerGraph)
=====================================

Goal: detect suspicious UPI/wallet-style rings via shared devices/IPs/phones and money-flow paths.

Contents
- gsql/schema_and_jobs.gsql — schema + loading job.
- gsql/queries.gsql — ring detection, alert explanation, mule ranking.
- data/generate_data.py — synthetic dataset generator (plants mule rings).

Quick start (local Docker container `tg`)
1) Generate data (makes CSVs under data/):
   ```
   cd fraud-ring-demo
   python3 data/generate_data.py
   ```
2) Copy folder into the container:
   ```
   docker cp fraud-ring-demo tg:/home/tigergraph/fraud-ring-demo
   ```
3) Inside container as tigergraph user, create graph + load data:
   ```
   docker exec -it -u tigergraph tg /home/tigergraph/tigergraph/app/cmd/gsql /home/tigergraph/fraud-ring-demo/gsql/schema_and_jobs.gsql
   docker exec -it -u tigergraph tg /home/tigergraph/tigergraph/app/cmd/gsql /home/tigergraph/fraud-ring-demo/gsql/queries.gsql
   ```
4) Run queries (examples):
   ```
   docker exec -it -u tigergraph tg /home/tigergraph/tigergraph/app/cmd/gsql "USE GRAPH Fraud; RUN QUERY ringDetect(\"acct_0001\", 2, 10)"
   docker exec -it -u tigergraph tg /home/tigergraph/tigergraph/app/cmd/gsql "USE GRAPH Fraud; RUN QUERY alertExplain(\"acct_0001\", 3)"
   docker exec -it -u tigergraph tg /home/tigergraph/tigergraph/app/cmd/gsql "USE GRAPH Fraud; RUN QUERY muleRanking(10)"
   ```

REST++
- After installing queries, you can hit:  
  `http://localhost:9000/query/Fraud/ringDetect?src=acct_0001&min_shared=2&top_k=10`

Notes
- Password currently set to `Hackathon123` for user `tigergraph` (change if needed).
- Dataset size defaults to ~2k accounts / 6k txns; adjust in generate_data.py if you want larger. 
