# Fair Management System (CLI)

## Overview
This project implements a small fair management system with a command-line
interface and JSON persistence. It supports vendors, stalls, products, and
sales with a simple commission model for the fair organizer.

## Domain Model (OOP Analysis)
- Fair: name, location, commission rate, and organizer balance.
- Vendor: name, balance, and assigned stalls.
- Stall: name, fee, and optional vendor owner.
- Product: name, price, quantity, and vendor owner.
- Sale: product, buyer, quantity, totals, commission, and timestamp.

Relationships:
- A vendor can own multiple stalls and products.
- A stall can be assigned to at most one vendor.
- A sale is linked to a product and its vendor.

## Business Rules
- Names are required and non-empty.
- Money values are non-negative; prices and quantities must be positive.
- A sale cannot exceed available stock.
- Commission rate is a percentage from 0 to 100.

## CLI Usage
Default data file: `fair_data.json` in the current directory.
Use `--data` to point to a different JSON file.

Initialize fair settings:
```bash
python -m lab1 init --name "City Fair" --location "Downtown" --commission 5
```

Add entities:
```bash
python -m lab1 add-vendor --name "Alice"
python -m lab1 add-stall --name "Hall A" --fee 10
python -m lab1 assign-stall --stall-id ST0001 --vendor-id V0001
python -m lab1 add-product --vendor-id V0001 --name "Apple" --price 2.50 --quantity 20
```

Record a sale:
```bash
python -m lab1 sell --product-id P0001 --quantity 3 --buyer "Bob"
```

List data:
```bash
python -m lab1 list vendors
python -m lab1 list stalls
python -m lab1 list products
python -m lab1 list sales
```

Reports:
```bash
python -m lab1 report
python -m lab1 vendor-report --vendor-id V0001
```

## Data Storage
All data is stored in a single JSON file. The file keeps fair settings,
entities, sales history, and internal counters for ID generation.

## Tests
Install test dependencies (optional):
```bash
pip install -e .[dev]
```

Run tests:
```bash
pytest
```
