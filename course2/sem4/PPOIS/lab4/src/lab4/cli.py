from __future__ import annotations

import argparse
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Sequence

from .application import FairApplication
from .errors import FairError

DEFAULT_DATA_FILE = "fair_data.json"


def decimal_arg(value: str) -> Decimal:
    try:
        return Decimal(value)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError("Value must be a decimal number.") from exc


def positive_int_arg(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Value must be an integer.") from exc
    if number <= 0:
        raise argparse.ArgumentTypeError("Value must be positive.")
    return number


def format_money(value: Decimal) -> str:
    return format(value, ".2f")


def format_percent(value: Decimal) -> str:
    return f"{format(value, '.2f')}%"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Open market management CLI")
    parser.add_argument(
        "--data",
        default=DEFAULT_DATA_FILE,
        help="Path to JSON data file.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize market settings.")
    init_parser.add_argument("--name", required=True, help="Market name.")
    init_parser.add_argument(
        "--location", default="Unknown", help="Market location."
    )
    init_parser.add_argument(
        "--commission",
        type=decimal_arg,
        default=Decimal("0.00"),
        help="Commission rate (percent).",
    )

    venue_parser = subparsers.add_parser("add-venue", help="Add a venue.")
    venue_parser.add_argument("--name", required=True, help="Venue name.")
    venue_parser.add_argument(
        "--location", default="Unknown", help="Venue location."
    )

    vendor_parser = subparsers.add_parser("add-vendor", help="Add a trader.")
    vendor_parser.add_argument("--name", required=True, help="Trader name.")

    trader_parser = subparsers.add_parser("add-trader", help="Add a trader.")
    trader_parser.add_argument("--name", required=True, help="Trader name.")

    buyer_parser = subparsers.add_parser("add-buyer", help="Add a buyer.")
    buyer_parser.add_argument("--name", required=True, help="Buyer name.")

    stall_parser = subparsers.add_parser("add-stall", help="Add a stall.")
    stall_parser.add_argument("--name", required=True, help="Stall name.")
    stall_parser.add_argument(
        "--fee",
        type=decimal_arg,
        default=Decimal("0.00"),
        help="Stall fee.",
    )
    stall_parser.add_argument("--venue-id", help="Venue id.", default=None)

    assign_parser = subparsers.add_parser(
        "assign-stall", help="Assign stall to vendor."
    )
    assign_parser.add_argument("--stall-id", required=True)
    assign_parser.add_argument("--vendor-id", required=True)

    product_parser = subparsers.add_parser("add-product", help="List a good.")
    product_parser.add_argument("--vendor-id", required=True)
    product_parser.add_argument("--name", required=True)
    product_parser.add_argument("--price", type=decimal_arg, required=True)
    product_parser.add_argument("--quantity", type=positive_int_arg, required=True)

    goods_parser = subparsers.add_parser("add-good", help="List a good.")
    goods_parser.add_argument("--vendor-id", required=True)
    goods_parser.add_argument("--name", required=True)
    goods_parser.add_argument("--price", type=decimal_arg, required=True)
    goods_parser.add_argument("--quantity", type=positive_int_arg, required=True)

    list_parser = subparsers.add_parser("list", help="List stored entities.")
    list_parser.add_argument(
        "entity",
        choices=[
            "vendors",
            "traders",
            "buyers",
            "venues",
            "stalls",
            "products",
            "goods",
            "sales",
            "promotions",
            "attractions",
        ],
    )

    sell_parser = subparsers.add_parser("sell", help="Record a sale.")
    sell_parser.add_argument("--product-id", required=True)
    sell_parser.add_argument("--quantity", type=positive_int_arg, required=True)
    sell_parser.add_argument("--buyer", default="Anonymous")

    trade_parser = subparsers.add_parser(
        "trade", help="Record a trade with optional negotiated price."
    )
    trade_parser.add_argument("--product-id", required=True)
    trade_parser.add_argument("--quantity", type=positive_int_arg, required=True)
    trade_parser.add_argument("--buyer", default=None)
    trade_parser.add_argument("--buyer-id", default=None)
    trade_parser.add_argument("--price", type=decimal_arg, default=None)

    advertise_parser = subparsers.add_parser(
        "advertise", help="Advertise the market event."
    )
    advertise_parser.add_argument("--message", required=True)

    attraction_parser = subparsers.add_parser(
        "add-attraction", help="Organize an attraction or entertainment."
    )
    attraction_parser.add_argument("--name", required=True)
    attraction_parser.add_argument("--description", default="")
    attraction_parser.add_argument("--venue-id", default=None)

    load_parser = subparsers.add_parser(
        "load-goods", help="Load goods (increase stock)."
    )
    load_parser.add_argument("--product-id", required=True)
    load_parser.add_argument("--quantity", type=positive_int_arg, required=True)

    unload_parser = subparsers.add_parser(
        "unload-goods", help="Unload goods (decrease stock)."
    )
    unload_parser.add_argument("--product-id", required=True)
    unload_parser.add_argument("--quantity", type=positive_int_arg, required=True)

    report_parser = subparsers.add_parser("report", help="Show market summary.")
    report_parser.add_argument(
        "--details",
        action="store_true",
        help="Include lists of traders and goods.",
    )

    vendor_report_parser = subparsers.add_parser(
        "vendor-report", help="Show vendor summary."
    )
    vendor_report_parser.add_argument("--vendor-id", required=True)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    app = FairApplication.from_path(Path(args.data))

    try:
        if args.command == "init":
            app.init_fair(args.name, args.location, args.commission)
            print("Market settings updated.")
        elif args.command == "add-venue":
            venue = app.create_venue(args.name, args.location)
            print(f"Venue created: {venue.venue_id} ({venue.name})")
        elif args.command in {"add-vendor", "add-trader"}:
            vendor = app.create_vendor(args.name)
            print(f"Trader created: {vendor.vendor_id} ({vendor.name})")
        elif args.command == "add-buyer":
            buyer = app.create_buyer(args.name)
            print(f"Buyer created: {buyer.buyer_id} ({buyer.name})")
        elif args.command == "add-stall":
            stall = app.create_stall(args.name, args.fee, args.venue_id)
            print(f"Stall created: {stall.stall_id} ({stall.name})")
        elif args.command == "assign-stall":
            stall = app.assign_stall(args.stall_id, args.vendor_id)
            print(
                f"Stall {stall.stall_id} assigned to trader {stall.vendor_id}."
            )
        elif args.command in {"add-product", "add-good"}:
            product = app.add_product(
                args.vendor_id, args.name, args.price, args.quantity
            )
            print(f"Good listed: {product.product_id} ({product.name})")
        elif args.command == "list":
            if args.entity in {"vendors", "traders"}:
                vendors = app.list_vendors()
                if not vendors:
                    print("No traders.")
                else:
                    print("Traders:")
                    for vendor in vendors:
                        print(
                            f"{vendor.vendor_id} | {vendor.name} | "
                            f"balance {format_money(vendor.balance)} | "
                            f"stalls {len(vendor.stall_ids)}"
                        )
            elif args.entity == "buyers":
                buyers = app.list_buyers()
                if not buyers:
                    print("No buyers.")
                else:
                    print("Buyers:")
                    for buyer in buyers:
                        print(f"{buyer.buyer_id} | {buyer.name}")
            elif args.entity == "venues":
                venues = app.list_venues()
                if not venues:
                    print("No venues.")
                else:
                    print("Venues:")
                    for venue in venues:
                        print(
                            f"{venue.venue_id} | {venue.name} | "
                            f"location {venue.location}"
                        )
            elif args.entity == "stalls":
                stalls = app.list_stalls()
                if not stalls:
                    print("No stalls.")
                else:
                    print("Stalls:")
                    for stall in stalls:
                        owner = stall.vendor_id or "-"
                        venue = stall.venue_id or "-"
                        print(
                            f"{stall.stall_id} | {stall.name} | "
                            f"fee {format_money(stall.fee)} | "
                            f"trader {owner} | "
                            f"venue {venue}"
                        )
            elif args.entity in {"products", "goods"}:
                products = app.list_products()
                if not products:
                    print("No goods.")
                else:
                    print("Goods:")
                    for product in products:
                        print(
                            f"{product.product_id} | {product.name} | "
                            f"trader {product.vendor_id} | "
                            f"price {format_money(product.price)} | "
                            f"qty {product.quantity}"
                        )
            elif args.entity == "promotions":
                promotions = app.list_promotions()
                if not promotions:
                    print("No promotions.")
                else:
                    print("Promotions:")
                    for promotion in promotions:
                        print(
                            f"{promotion.promotion_id} | "
                            f"{promotion.message} | "
                            f"time {promotion.timestamp}"
                        )
            elif args.entity == "attractions":
                attractions = app.list_attractions()
                if not attractions:
                    print("No attractions.")
                else:
                    print("Attractions:")
                    for attraction in attractions:
                        venue = attraction.venue_id or "-"
                        description = attraction.description or "-"
                        print(
                            f"{attraction.attraction_id} | {attraction.name} | "
                            f"venue {venue} | {description}"
                        )
            else:
                sales = app.list_sales()
                if not sales:
                    print("No sales.")
                else:
                    print("Sales:")
                    for sale in sales:
                        buyer_label = sale.buyer_id or sale.buyer
                        print(
                            f"{sale.sale_id} | product {sale.product_id} | "
                            f"buyer {buyer_label} | qty {sale.quantity} | "
                            f"total {format_money(sale.total)} | "
                            f"commission {format_money(sale.commission)} | "
                            f"time {sale.timestamp}"
                        )
        elif args.command == "sell":
            sale = app.sell(args.product_id, args.quantity, args.buyer)
            print(
                f"Sale recorded: {sale.sale_id} total "
                f"{format_money(sale.total)}"
            )
        elif args.command == "trade":
            sale = app.trade(
                args.product_id,
                args.quantity,
                buyer=args.buyer,
                buyer_id=args.buyer_id,
                unit_price=args.price,
            )
            print(
                f"Trade recorded: {sale.sale_id} total "
                f"{format_money(sale.total)}"
            )
        elif args.command == "advertise":
            promotion = app.advertise_event(args.message)
            print(
                f"Promotion created: {promotion.promotion_id} "
                f"({promotion.message})"
            )
        elif args.command == "add-attraction":
            attraction = app.add_attraction(
                args.name, args.description, args.venue_id
            )
            print(
                f"Attraction created: {attraction.attraction_id} "
                f"({attraction.name})"
            )
        elif args.command == "load-goods":
            product = app.load_goods(args.product_id, args.quantity)
            print(
                f"Goods loaded: {product.product_id} qty {product.quantity}"
            )
        elif args.command == "unload-goods":
            product = app.unload_goods(args.product_id, args.quantity)
            print(
                f"Goods unloaded: {product.product_id} qty {product.quantity}"
            )
        elif args.command == "report":
            fair = app.fair
            summary = app.summary()
            print(f"Market: {fair.name} ({fair.location})")
            print(f"Commission rate: {format_percent(fair.commission_rate)}")
            print(f"Market balance: {format_money(fair.balance)}")
            print(
                "Entities: "
                f"traders {summary['vendors']} | "
                f"buyers {summary['buyers']} | "
                f"venues {summary['venues']} | "
                f"stalls {summary['stalls']} | "
                f"goods {summary['products']} | "
                f"sales {summary['sales']} | "
                f"promotions {summary['promotions']} | "
                f"attractions {summary['attractions']}"
            )
            print(f"Total sales: {format_money(summary['total_sales'])}")
            print(
                "Total commission: "
                f"{format_money(summary['total_commission'])}"
            )
            if args.details:
                vendors = app.list_vendors()
                if vendors:
                    print("Traders:")
                    for vendor in vendors:
                        print(
                            f"{vendor.vendor_id} | {vendor.name} | "
                            f"balance {format_money(vendor.balance)}"
                        )
                products = app.list_products()
                if products:
                    print("Goods:")
                    for product in products:
                        print(
                            f"{product.product_id} | {product.name} | "
                            f"price {format_money(product.price)} | "
                            f"qty {product.quantity}"
                        )
        elif args.command == "vendor-report":
            report = app.vendor_report(args.vendor_id)
            print(
                f"Trader {report['vendor_id']} - {report['name']}"
            )
            print(f"Balance: {format_money(report['balance'])}")
            print(f"Sales count: {report['sales_count']}")
            print(f"Total sales: {format_money(report['total_sales'])}")
            print(f"Products: {report['products_count']}")
            print(f"Stalls: {report['stalls_count']}")
        else:
            parser.error("Unknown command.")
    except FairError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0
