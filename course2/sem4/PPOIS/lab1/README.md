# Open Market Management System (CLI)

## Overview
This project implements a small open market management system with a
command-line interface and JSON persistence. It supports traders, buyers,
venues, stalls, goods, and trades with a simple commission model for the
market organizer. It also tracks promotions and attractions.

## Domain Model (OOP Analysis)
- Market (Fair): name, location, commission rate, and organizer balance.
- Venue: name and location.
- Trader (Vendor): name, balance, and assigned stalls.
- Buyer: name.
- Stall: name, fee, optional trader owner, optional venue.
- Good (Product): name, price, quantity, and trader owner.
- Trade (Sale): good, buyer, quantity, negotiated price, totals, commission,
  and timestamp.
- Promotion: advertising message and timestamp.
- Attraction: name, optional description, optional venue.

Relationships:
- A trader can own multiple stalls and goods.
- A stall can be assigned to at most one trader and can belong to a venue.
- A trade is linked to a good and its trader.

## Business Rules
- Names are required and non-empty.
- Money values are non-negative; prices and quantities must be positive.
- A trade cannot exceed available stock.
- Commission rate is a percentage from 0 to 100.

## CLI Usage
Default data file: `fair_data.json` in the current directory.
Use `--data` to point to a different JSON file.

Initialize market settings:
```bash
python -m lab1 init --name "City Fair" --location "Downtown" --commission 5
```

Add entities:
```bash
python -m lab1 add-venue --name "Main Square" --location "Downtown"
python -m lab1 add-trader --name "Alice"
python -m lab1 add-buyer --name "Bob"
python -m lab1 add-stall --name "Hall A" --fee 10
python -m lab1 assign-stall --stall-id ST0001 --vendor-id V0001
python -m lab1 add-good --vendor-id V0001 --name "Apple" --price 2.50 --quantity 20
```

Record a trade with optional negotiated price:
```bash
python -m lab1 trade --product-id P0001 --quantity 3 --buyer-id B0001 --price 2.20
```

List data:
```bash
python -m lab1 list traders
python -m lab1 list buyers
python -m lab1 list venues
python -m lab1 list stalls
python -m lab1 list goods
python -m lab1 list sales
python -m lab1 list promotions
python -m lab1 list attractions
```

Advertising and attractions:
```bash
python -m lab1 advertise --message "Open market this Saturday!"
python -m lab1 add-attraction --name "Street Music" --description "Live band"
```

Load/unload goods:
```bash
python -m lab1 load-goods --product-id P0001 --quantity 5
python -m lab1 unload-goods --product-id P0001 --quantity 2
```

Reports:
```bash
python -m lab1 report
python -m lab1 vendor-report --vendor-id V0001
```

## Data Storage
All data is stored in a single JSON file. The file keeps market settings,
entities, trades, promotions, attractions, and internal counters for ID
generation.

## Tests
Install test dependencies (optional):
```bash
pip install -e .[dev]
```

Run tests:
```bash
pytest
```
