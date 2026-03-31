const fs = require("fs");
const path = require("path");

let cache = null;

function readCsv(filePath) {
  const text = fs.readFileSync(filePath, "utf8").trim();
  if (!text) return [];
  return text.split(/\r?\n/).map((line) => line.split(","));
}

function loadData() {
  if (cache) return cache;

  const dataDir = path.join(process.cwd(), "fraud-ring-demo", "data");
  const accounts = new Map();
  const devices = new Map();
  const ips = new Map();
  const phones = new Map();
  const outDeg = new Map();
  const inDeg = new Map();

  for (const [pid, flagged, _createdAt, riskScore] of readCsv(path.join(dataDir, "accounts.csv"))) {
    accounts.set(pid, {
      pid,
      flagged: Number(flagged || 0),
      risk_score: Number(riskScore || 0),
    });
  }

  for (const [acct, device] of readCsv(path.join(dataDir, "account_device.csv"))) {
    if (!devices.has(acct)) devices.set(acct, new Set());
    devices.get(acct).add(device);
  }
  for (const [acct, ip] of readCsv(path.join(dataDir, "account_ip.csv"))) {
    if (!ips.has(acct)) ips.set(acct, new Set());
    ips.get(acct).add(ip);
  }
  for (const [acct, phone] of readCsv(path.join(dataDir, "account_phone.csv"))) {
    if (!phones.has(acct)) phones.set(acct, new Set());
    phones.get(acct).add(phone);
  }
  for (const [src, dst] of readCsv(path.join(dataDir, "transfers.csv"))) {
    outDeg.set(src, (outDeg.get(src) || 0) + 1);
    inDeg.set(dst, (inDeg.get(dst) || 0) + 1);
  }

  cache = { accounts, devices, ips, phones, outDeg, inDeg };
  return cache;
}

module.exports = (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET,OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(204).end();
  }
  if (req.method !== "GET") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { accounts, devices, ips, phones, outDeg, inDeg } = loadData();
  const src = String(req.query.src || "").trim();
  const minShared = Number(req.query.min_shared || 2);
  const topK = Number(req.query.top_k || 10);

  if (!src || !accounts.has(src)) {
    return res.status(200).json({ results: [{ ordered: [] }] });
  }

  const srcDevices = devices.get(src) || new Set();
  const srcIps = ips.get(src) || new Set();
  const srcPhones = phones.get(src) || new Set();

  const rows = [];
  for (const [acct, meta] of accounts.entries()) {
    if (acct === src) continue;
    const sharedCount =
      [...srcDevices].filter((value) => (devices.get(acct) || new Set()).has(value)).length +
      [...srcPhones].filter((value) => (phones.get(acct) || new Set()).has(value)).length +
      [...srcIps].filter((value) => (ips.get(acct) || new Set()).has(value)).length;

    if (sharedCount < minShared) continue;

    rows.push({
      attributes: {
        pid: meta.pid,
        flagged: meta.flagged,
        risk_score: meta.risk_score,
        "@shared_count": sharedCount,
        "@deg_out": outDeg.get(acct) || 0,
        "@deg_in": inDeg.get(acct) || 0,
      },
    });
  }

  rows.sort((a, b) => {
    const aa = a.attributes;
    const bb = b.attributes;
    return (
      bb["@shared_count"] - aa["@shared_count"] ||
      bb["@deg_out"] - aa["@deg_out"] ||
      bb["@deg_in"] - aa["@deg_in"] ||
      String(aa.pid).localeCompare(String(bb.pid))
    );
  });

  return res.status(200).json({ results: [{ ordered: rows.slice(0, topK) }] });
};
