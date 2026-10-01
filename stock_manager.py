import argparse
import csv
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TRANSACTIONS_FILE = DATA_DIR / "transactions.csv"
CSV_HEADERS = [
    "date",
    "item",
    "item_code",
    "in_qty",
    "out_qty",
    "unit",
    "party",
    "remarks",
]


def ensure_data_file():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not TRANSACTIONS_FILE.exists():
        with TRANSACTIONS_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writeheader()


def load_transactions():
    ensure_data_file()
    rows = []
    with TRANSACTIONS_FILE.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row or all((value is None or str(value).strip() == "") for value in row.values()):
                continue
            rows.append({
                "date": (row.get("date") or "").strip(),
                "item": (row.get("item") or "").strip(),
                "item_code": (row.get("item_code") or "").strip(),
                "in_qty": int(row.get("in_qty") or 0),
                "out_qty": int(row.get("out_qty") or 0),
                "unit": (row.get("unit") or "").strip(),
                "party": (row.get("party") or "").strip(),
                "remarks": (row.get("remarks") or "").strip(),
            })
    return rows


def save_transaction(row):
    ensure_data_file()
    with TRANSACTIONS_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writerow(row)


def summary_by_item(rows):
    summary = defaultdict(lambda: {
        "item": "",
        "item_code": "",
        "unit": "",
        "in_qty": 0,
        "out_qty": 0,
    })

    for row in rows:
        key = row["item_code"] or row["item"]
        item_row = summary[key]
        item_row["item"] = row["item"]
        item_row["item_code"] = row["item_code"]
        item_row["unit"] = row["unit"]
        item_row["in_qty"] += row["in_qty"]
        item_row["out_qty"] += row["out_qty"]

    results = []
    for key, item_row in summary.items():
        results.append({
            "item": item_row["item"],
            "item_code": item_row["item_code"],
            "unit": item_row["unit"],
            "total_in": item_row["in_qty"],
            "total_out": item_row["out_qty"],
            "stock": item_row["in_qty"] - item_row["out_qty"],
        })
    return sorted(results, key=lambda x: (x["item"], x["item_code"]))


def list_transactions():
    rows = load_transactions()
    if not rows:
        print("No transaction records found.")
        return
    print("Date | Item | Code | In Qty | Out Qty | Unit | Party | Remarks")
    print("-" * 140)
    for row in rows:
        print(
            f"{row['date']} | {row['item']} | {row['item_code']} | {row['in_qty']} | {row['out_qty']} | "
            f"{row['unit']} | {row['party']} | {row['remarks']}"
        )


def show_summary():
    rows = load_transactions()
    summary = summary_by_item(rows)
    if not summary:
        print("No stock summary available.")
        return
    print("Item | Code | Unit | Total In | Total Out | Stock")
    print("-" * 120)
    for item in summary:
        print(
            f"{item['item']} | {item['item_code']} | {item['unit']} | {item['total_in']} | {item['total_out']} | {item['stock']}"
        )


def add_transaction(args):
    row = {
        "date": args.date,
        "item": args.item,
        "item_code": args.item_code,
        "in_qty": args.in_qty,
        "out_qty": args.out_qty,
        "unit": args.unit,
        "party": args.party,
        "remarks": args.remarks,
    }
    save_transaction(row)
    print("Transaction added successfully.")


def build_parser():
    parser = argparse.ArgumentParser(description="Simple in/out stock list manager.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a stock transaction")
    add_parser.add_argument("--date", required=True, help="Transaction date, e.g. 2026-10-01")
    add_parser.add_argument("--item", required=True, help="Item name")
    add_parser.add_argument("--item_code", required=True, help="Item code")
    add_parser.add_argument("--in_qty", type=int, default=0, help="Incoming quantity")
    add_parser.add_argument("--out_qty", type=int, default=0, help="Outgoing quantity")
    add_parser.add_argument("--unit", default="pcs", help="Units, e.g. pcs, box, kg")
    add_parser.add_argument("--party", default="", help="Supplier or customer")
    add_parser.add_argument("--remarks", default="", help="Remarks")
    add_parser.set_defaults(func=add_transaction)

    list_parser = subparsers.add_parser("list", help="List all transactions")
    list_parser.set_defaults(func=lambda _args: list_transactions())

    summary_parser = subparsers.add_parser("summary", help="Show current stock summary")
    summary_parser.set_defaults(func=lambda _args: show_summary())

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
