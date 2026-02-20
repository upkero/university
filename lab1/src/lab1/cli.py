from __future__ import annotations

import argparse
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Sequence

from .errors import FairError
from .service import FairService
from .storage import DataStore

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
    parser = argparse.ArgumentParser(description="Fair management CLI")
    parser.add_argument(
        "--data",
        default=DEFAULT_DATA_FILE,
        help="Path to JSON data file.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize fair settings.")
    init_parser.add_argument("--name", required=True, help="Fair name.")
    init_parser.add_argument(
        "--location", default="Unknown", help="Fair location."
    )
    init_parser.add_argument(
        "--commission",
        type=decimal_arg,
        default=Decimal("0.00"),
        help="Commission rate (percent).",
    )

    vendor_parser = subparsers.add_parser("add-vendor", help="Add a vendor.")
    vendor_parser.add_argument("--name", required=True, help="Vendor name.")

    stall_parser = subparsers.add_parser("add-stall", help="Add a stall.")
    stall_parser.add_argument("--name", required=True, help="Stall name.")
    stall_parser.add_argument(
        "--fee",
        type=decimal_arg,
        default=Decimal("0.00"),
        help="Stall fee.",
    )

    assign_parser = subparsers.add_parser(
        "assign-stall", help="Assign stall to vendor."
    )
    assign_parser.add_argument("--stall-id", required=True)
    assign_parser.add_argument("--vendor-id", required=True)

    product_parser = subparsers.add_parser("add-product", help="Add a product.")
    product_parser.add_argument("--vendor-id", required=True)
    product_parser.add_argument("--name", required=True)
    product_parser.add_argument("--price", type=decimal_arg, required=True)
    product_parser.add_argument("--quantity", type=positive_int_arg, required=True)

    list_parser = subparsers.add_parser("list", help="List stored entities.")
    list_parser.add_argument(
        "entity", choices=["vendors", "stalls", "products", "sales"]
    )

    sell_parser = subparsers.add_parser("sell", help="Record a sale.")
    sell_parser.add_argument("--product-id", required=True)
    sell_parser.add_argument("--quantity", type=positive_int_arg, required=True)
    sell_parser.add_argument("--buyer", default="Anonymous")

    report_parser = subparsers.add_parser("report", help="Show fair summary.")
    report_parser.add_argument(
        "--details",
        action="store_true",
        help="Include lists of vendors and products.",
    )

    vendor_report_parser = subparsers.add_parser(
        "vendor-report", help="Show vendor summary."
    )
    vendor_report_parser.add_argument("--vendor-id", required=True)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = DataStore(Path(args.data))
    data = store.load()
    service = FairService(data)
    should_save = False

    try:
        if args.command == "init":
            service.init_fair(args.name, args.location, args.commission)
            should_save = True
            print("Fair settings updated.")
        elif args.command == "add-vendor":
            vendor = service.create_vendor(args.name)
            should_save = True
            print(f"Vendor created: {vendor.vendor_id} ({vendor.name})")
        elif args.command == "add-stall":
            stall = service.create_stall(args.name, args.fee)
            should_save = True
            print(f"Stall created: {stall.stall_id} ({stall.name})")
        elif args.command == "assign-stall":
            stall = service.assign_stall(args.stall_id, args.vendor_id)
            should_save = True
            print(
                f"Stall {stall.stall_id} assigned to vendor {stall.vendor_id}."
            )
        elif args.command == "add-product":
            product = service.add_product(
                args.vendor_id, args.name, args.price, args.quantity
            )
            should_save = True
            print(
                f"Product created: {product.product_id} ({product.name})"
            )
        elif args.command == "list":
            if args.entity == "vendors":
                vendors = service.list_vendors()
                if not vendors:
                    print("No vendors.")
                else:
                    print("Vendors:")
                    for vendor in vendors:
                        print(
                            f"{vendor.vendor_id} | {vendor.name} | "
                            f"balance {format_money(vendor.balance)} | "
                            f"stalls {len(vendor.stall_ids)}"
                        )
            elif args.entity == "stalls":
                stalls = service.list_stalls()
                if not stalls:
                    print("No stalls.")
                else:
                    print("Stalls:")
                    for stall in stalls:
                        owner = stall.vendor_id or "-"
                        print(
                            f"{stall.stall_id} | {stall.name} | "
                            f"fee {format_money(stall.fee)} | "
                            f"vendor {owner}"
                        )
            elif args.entity == "products":
                products = service.list_products()
                if not products:
                    print("No products.")
                else:
                    print("Products:")
                    for product in products:
                        print(
                            f"{product.product_id} | {product.name} | "
                            f"vendor {product.vendor_id} | "
                            f"price {format_money(product.price)} | "
                            f"qty {product.quantity}"
                        )
            else:
                sales = service.list_sales()
                if not sales:
                    print("No sales.")
                else:
                    print("Sales:")
                    for sale in sales:
                        print(
                            f"{sale.sale_id} | product {sale.product_id} | "
                            f"buyer {sale.buyer} | qty {sale.quantity} | "
                            f"total {format_money(sale.total)} | "
                            f"commission {format_money(sale.commission)} | "
                            f"time {sale.timestamp}"
                        )
        elif args.command == "sell":
            sale = service.sell(args.product_id, args.quantity, args.buyer)
            should_save = True
            print(
                f"Sale recorded: {sale.sale_id} total "
                f"{format_money(sale.total)}"
            )
        elif args.command == "report":
            fair = data.fair
            summary = service.summary()
            print(f"Fair: {fair.name} ({fair.location})")
            print(f"Commission rate: {format_percent(fair.commission_rate)}")
            print(f"Fair balance: {format_money(fair.balance)}")
            print(
                "Entities: "
                f"vendors {summary['vendors']} | "
                f"stalls {summary['stalls']} | "
                f"products {summary['products']} | "
                f"sales {summary['sales']}"
            )
            print(f"Total sales: {format_money(summary['total_sales'])}")
            print(
                "Total commission: "
                f"{format_money(summary['total_commission'])}"
            )
            if args.details:
                vendors = service.list_vendors()
                if vendors:
                    print("Vendors:")
                    for vendor in vendors:
                        print(
                            f"{vendor.vendor_id} | {vendor.name} | "
                            f"balance {format_money(vendor.balance)}"
                        )
                products = service.list_products()
                if products:
                    print("Products:")
                    for product in products:
                        print(
                            f"{product.product_id} | {product.name} | "
                            f"price {format_money(product.price)} | "
                            f"qty {product.quantity}"
                        )
        elif args.command == "vendor-report":
            report = service.vendor_report(args.vendor_id)
            print(
                f"Vendor {report['vendor_id']} - {report['name']}"
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

    if should_save:
        store.save(data)
    return 0
