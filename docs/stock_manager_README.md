# Simple Stock Manager

This project is a minimal stock management tool for recording in/out stock and calculating current inventory.

## Features
- Add stock in and stock out transactions
- Store records in CSV
- Show all transactions
- Generate current stock summary

## Files
- `stock_manager.py` - CLI program
- `data/transactions.csv` - transaction records

## Quick Start

1. View transactions:
   python stock_manager.py list

2. Add stock in:
   python stock_manager.py add --date 2026-10-01 --item "A4纸" --item_code SKU-001 --in_qty 100 --unit 包 --party "ABC Paper" --remarks "进货"

3. Add stock out:
   python stock_manager.py add --date 2026-10-02 --item "A4纸" --item_code SKU-001 --out_qty 20 --unit 包 --party "Office" --remarks "办公使用"

4. View stock summary:
   python stock_manager.py summary

## CSV Format
The transaction file uses these columns:

`date,item,item_code,in_qty,out_qty,unit,party,remarks`
