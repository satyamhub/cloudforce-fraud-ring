Quickstart demo for TigerGraph 4.2.2 (Docker)

Files here assume you start a container named `tg` from the provided image and then enter it with:

```
docker exec -it tg bash
su - tigergraph
```

Run the scripts in this order inside the container:

1) Create schema and loading job
```
gsql /home/tigergraph/quickstart-demo/schema_and_loading.gsql
```

2) Load the sample data (people.csv) into the Demo graph
```
gsql /home/tigergraph/quickstart-demo/load_data.gsql
```

3) Install and run the sample query that walks 2 hops in the social graph
```
gsql /home/tigergraph/quickstart-demo/sample_query.gsql
curl -u tigergraph:<your_pass> "http://localhost:9000/query/Demo/twoHop?src=Alice"
```

Copy this folder into the container (one-time):
```
docker cp quickstart-demo tg:/home/tigergraph/
```

Notes
- Current TigerGraph password (set for user `tigergraph`): `Hackathon123`.
- `people.csv` is tiny so you can reload quickly during the hackathon.
- If you rerun schema script, drop the graph first: `gsql "DROP GRAPH Demo"`.
