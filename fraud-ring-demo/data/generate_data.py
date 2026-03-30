import csv
import random
import datetime
from pathlib import Path

random.seed(42)

OUT_DIR = Path(__file__).parent

# sizes (tweak if needed)
N_ACCTS = 2000
N_DEVICES = 800
N_IPS = 600
N_PHONES = 500
N_MERCH = 200
N_TXNS = 9000

RINGS = [
    {"size": 8, "shared_devices": 2, "shared_ips": 2},
    {"size": 10, "shared_devices": 3, "shared_ips": 2},
    {"size": 6, "shared_devices": 1, "shared_ips": 1},
]

def rand_date(start_year=2023):
    start = datetime.datetime(start_year, 1, 1)
    end = datetime.datetime(2026, 3, 1)
    delta = end - start
    return start + datetime.timedelta(days=random.randint(0, delta.days))


def make_ids(prefix, n):
    return [f"{prefix}_{i:04d}" for i in range(n)]


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def main():
    accounts = make_ids("acct", N_ACCTS)
    devices = make_ids("dev", N_DEVICES)
    ips = [f"10.0.{i//256}.{i%256}" for i in range(N_IPS)]
    phones = [f"+91{random.randint(7000000000, 9999999999)}" for _ in range(N_PHONES)]
    merchs = make_ids("merch", N_MERCH)

    # Flag a few merchants
    flagged_merch = set(random.sample(merchs, 5))

    # Account attributes
    account_rows = []
    for a in accounts:
        flagged = 0
        created_at = rand_date().strftime("%Y-%m-%d %H:%M:%S")
        risk = round(random.random() * 0.2, 3)
        account_rows.append([a, flagged, created_at, risk])

    # Seed rings
    account_device = []
    account_ip = []
    account_phone = []
    transfer_rows = []
    shops_rows = []
    flagged_accounts = set()

    offset = 0
    for ring in RINGS:
        size = ring["size"]
        members = accounts[offset : offset + size]
        offset += size
        shared_devs = random.sample(devices, ring["shared_devices"])
        shared_ips = random.sample(ips, ring["shared_ips"])
        shared_phone = random.choice(phones)

        # mark one member flagged
        flagged = random.choice(members)
        flagged_accounts.add(flagged)
        for row in account_rows:
            if row[0] == flagged:
                row[1] = 1
                row[3] = round(row[3] + 0.7, 3)

        for a in members:
            # everyone shares devices & ips
            for d in shared_devs:
                account_device.append([a, d])
            for ip in shared_ips:
                account_ip.append([a, ip])
            account_phone.append([a, shared_phone])

        # dense money transfers inside ring
        for i in range(len(members)):
            for j in range(len(members)):
                if i == j or random.random() < 0.4:
                    continue
                amt = round(random.uniform(200, 2000), 2)
                ts = rand_date().strftime("%Y-%m-%d %H:%M:%S")
                merch = random.choice(merchs)
                transfer_rows.append([members[i], members[j], amt, ts, merch])

    # Non-ring accounts random assets (wider fan-out)
    for a in accounts[offset:]:
        devs = random.sample(devices, random.randint(1, 4))
        ips_for_a = random.sample(ips, random.randint(1, 4))
        ph = random.choice(phones)
        for d in devs:
            account_device.append([a, d])
        for ip in ips_for_a:
            account_ip.append([a, ip])
        account_phone.append([a, ph])

    # Random txns overall
    for _ in range(N_TXNS):
        src, dst = random.sample(accounts, 2)
        amt = round(random.uniform(50, 5000), 2)
        ts = rand_date().strftime("%Y-%m-%d %H:%M:%S")
        merch = random.choice(merchs)
        transfer_rows.append([src, dst, amt, ts, merch])
        # shops edge (account -> merchant)
        shops_rows.append([src, merch, amt, ts])
        # occasionally add a burst of extra txns to increase outdegree
        if random.random() < 0.15:
            for _ in range(random.randint(1, 3)):
                dst2 = random.choice(accounts)
                amt2 = round(random.uniform(50, 3000), 2)
                ts2 = rand_date().strftime("%Y-%m-%d %H:%M:%S")
                transfer_rows.append([src, dst2, amt2, ts2, merch])

    # Merchants
    merch_rows = []
    for m in merchs:
        merch_rows.append([m, 1 if m in flagged_merch else 0])

    # Devices, IPs, Phones vertices
    device_rows = [[d] for d in devices]
    ip_rows = [[ip] for ip in ips]
    phone_rows = [[p] for p in phones]

    # Write files
    write_csv(OUT_DIR / "accounts.csv", account_rows)
    write_csv(OUT_DIR / "devices.csv", device_rows)
    write_csv(OUT_DIR / "ips.csv", ip_rows)
    write_csv(OUT_DIR / "phones.csv", phone_rows)
    write_csv(OUT_DIR / "merchants.csv", merch_rows)
    write_csv(OUT_DIR / "account_device.csv", account_device)
    write_csv(OUT_DIR / "account_ip.csv", account_ip)
    write_csv(OUT_DIR / "account_phone.csv", account_phone)
    write_csv(OUT_DIR / "transfers.csv", transfer_rows)
    write_csv(OUT_DIR / "shops.csv", shops_rows)

    print("Generated CSVs in", OUT_DIR)
    print(f"Flagged accounts: {len(flagged_accounts)} | Flagged merchants: {len(flagged_merch)}")


if __name__ == "__main__":
    main()
