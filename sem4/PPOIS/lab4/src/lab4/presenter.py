from __future__ import annotations

from decimal import Decimal, InvalidOperation
from pathlib import Path

from .application import FairApplication
from .errors import ValidationError


def format_money(value: Decimal) -> str:
    return format(value, ".2f")


def format_percent(value: Decimal) -> str:
    return f"{format(value, '.2f')}%"


class FairPresenter:
    """MVP presenter for the GUI client."""

    def __init__(self, app: FairApplication) -> None:
        self._app = app

    @classmethod
    def from_path(cls, data_path: Path) -> "FairPresenter":
        return cls(FairApplication.from_path(data_path))

    def init_fair(self, name: str, location: str, commission_rate: str) -> str:
        commission = self._parse_decimal(commission_rate, "Commission rate")
        fair = self._app.init_fair(name, location, commission)
        return f"Market updated: {fair.name} ({fair.location})"

    def create_venue(self, name: str, location: str) -> str:
        venue = self._app.create_venue(name, location)
        return f"Venue created: {venue.venue_id} ({venue.name})"

    def create_vendor(self, name: str) -> str:
        vendor = self._app.create_vendor(name)
        return f"Trader created: {vendor.vendor_id} ({vendor.name})"

    def create_buyer(self, name: str) -> str:
        buyer = self._app.create_buyer(name)
        return f"Buyer created: {buyer.buyer_id} ({buyer.name})"

    def create_stall(self, name: str, fee: str, venue_id: str) -> str:
        stall_fee = self._parse_decimal(fee, "Stall fee")
        stall = self._app.create_stall(name, stall_fee, self._optional_text(venue_id))
        return f"Stall created: {stall.stall_id} ({stall.name})"

    def assign_stall(self, stall_id: str, vendor_id: str) -> str:
        stall = self._app.assign_stall(stall_id.strip(), vendor_id.strip())
        return f"Stall {stall.stall_id} assigned to trader {stall.vendor_id}"

    def add_product(
        self,
        vendor_id: str,
        name: str,
        price: str,
        quantity: str,
    ) -> str:
        product_price = self._parse_decimal(price, "Product price")
        product_quantity = self._parse_positive_int(quantity, "Product quantity")
        product = self._app.add_product(
            vendor_id.strip(),
            name,
            product_price,
            product_quantity,
        )
        return f"Good listed: {product.product_id} ({product.name})"

    def sell(self, product_id: str, quantity: str, buyer: str) -> str:
        sale_quantity = self._parse_positive_int(quantity, "Trade quantity")
        sale = self._app.sell(product_id.strip(), sale_quantity, buyer)
        return f"Sale recorded: {sale.sale_id}, total {format_money(sale.total)}"

    def trade(
        self,
        product_id: str,
        quantity: str,
        buyer: str,
        buyer_id: str,
        unit_price: str,
    ) -> str:
        sale_quantity = self._parse_positive_int(quantity, "Trade quantity")
        price = self._parse_optional_decimal(unit_price, "Negotiated price")
        sale = self._app.trade(
            product_id.strip(),
            sale_quantity,
            buyer=self._optional_text(buyer),
            buyer_id=self._optional_text(buyer_id),
            unit_price=price,
        )
        return f"Trade recorded: {sale.sale_id}, total {format_money(sale.total)}"

    def advertise_event(self, message: str) -> str:
        promotion = self._app.advertise_event(message)
        return f"Promotion created: {promotion.promotion_id}"

    def add_attraction(self, name: str, description: str, venue_id: str) -> str:
        attraction = self._app.add_attraction(
            name,
            description,
            self._optional_text(venue_id),
        )
        return f"Attraction created: {attraction.attraction_id}"

    def load_goods(self, product_id: str, quantity: str) -> str:
        amount = self._parse_positive_int(quantity, "Load quantity")
        product = self._app.load_goods(product_id.strip(), amount)
        return f"Goods loaded: {product.product_id}, qty {product.quantity}"

    def unload_goods(self, product_id: str, quantity: str) -> str:
        amount = self._parse_positive_int(quantity, "Unload quantity")
        product = self._app.unload_goods(product_id.strip(), amount)
        return f"Goods unloaded: {product.product_id}, qty {product.quantity}"

    def vendor_report_text(self, vendor_id: str) -> str:
        report = self._app.vendor_report(vendor_id.strip())
        return "\n".join(
            [
                f"Trader: {report['vendor_id']} - {report['name']}",
                f"Balance: {format_money(report['balance'])}",
                f"Sales count: {report['sales_count']}",
                f"Total sales: {format_money(report['total_sales'])}",
                f"Products: {report['products_count']}",
                f"Stalls: {report['stalls_count']}",
            ]
        )

    def summary_text(self) -> str:
        fair = self._app.fair
        summary = self._app.summary()
        lines = [
            f"Market: {fair.name}",
            f"Location: {fair.location}",
            f"Commission rate: {format_percent(fair.commission_rate)}",
            f"Market balance: {format_money(fair.balance)}",
            "",
            "Entities:",
            f"- Traders: {summary['vendors']}",
            f"- Buyers: {summary['buyers']}",
            f"- Venues: {summary['venues']}",
            f"- Stalls: {summary['stalls']}",
            f"- Goods: {summary['products']}",
            f"- Sales: {summary['sales']}",
            f"- Promotions: {summary['promotions']}",
            f"- Attractions: {summary['attractions']}",
            "",
            f"Total sales: {format_money(summary['total_sales'])}",
            f"Total commission: {format_money(summary['total_commission'])}",
        ]
        return "\n".join(lines)

    def vendors_rows(self) -> list[tuple[str, str, str, str]]:
        return [
            (
                vendor.vendor_id,
                vendor.name,
                format_money(vendor.balance),
                str(len(vendor.stall_ids)),
            )
            for vendor in self._app.list_vendors()
        ]

    def buyers_rows(self) -> list[tuple[str, str]]:
        return [
            (buyer.buyer_id, buyer.name)
            for buyer in self._app.list_buyers()
        ]

    def venues_rows(self) -> list[tuple[str, str, str]]:
        return [
            (venue.venue_id, venue.name, venue.location)
            for venue in self._app.list_venues()
        ]

    def stalls_rows(self) -> list[tuple[str, str, str, str, str]]:
        return [
            (
                stall.stall_id,
                stall.name,
                format_money(stall.fee),
                stall.vendor_id or "-",
                stall.venue_id or "-",
            )
            for stall in self._app.list_stalls()
        ]

    def products_rows(self) -> list[tuple[str, str, str, str, str]]:
        return [
            (
                product.product_id,
                product.name,
                product.vendor_id,
                format_money(product.price),
                str(product.quantity),
            )
            for product in self._app.list_products()
        ]

    def sales_rows(self) -> list[tuple[str, str, str, str, str, str, str, str, str]]:
        return [
            (
                sale.sale_id,
                sale.product_id,
                sale.vendor_id,
                sale.buyer_id or sale.buyer,
                str(sale.quantity),
                format_money(sale.unit_price),
                format_money(sale.total),
                format_money(sale.commission),
                sale.timestamp,
            )
            for sale in self._app.list_sales()
        ]

    def promotions_rows(self) -> list[tuple[str, str, str]]:
        return [
            (promotion.promotion_id, promotion.message, promotion.timestamp)
            for promotion in self._app.list_promotions()
        ]

    def attractions_rows(self) -> list[tuple[str, str, str, str]]:
        return [
            (
                attraction.attraction_id,
                attraction.name,
                attraction.description or "-",
                attraction.venue_id or "-",
            )
            for attraction in self._app.list_attractions()
        ]

    def _parse_decimal(self, value: str, field_name: str) -> Decimal:
        text = value.strip()
        if not text:
            raise ValidationError(f"{field_name} must not be empty.")
        try:
            return Decimal(text)
        except InvalidOperation as exc:
            raise ValidationError(
                f"{field_name} must be a decimal number."
            ) from exc

    def _parse_optional_decimal(
        self, value: str, field_name: str
    ) -> Decimal | None:
        text = value.strip()
        if not text:
            return None
        try:
            return Decimal(text)
        except InvalidOperation as exc:
            raise ValidationError(
                f"{field_name} must be a decimal number."
            ) from exc

    def _parse_positive_int(self, value: str, field_name: str) -> int:
        text = value.strip()
        if not text:
            raise ValidationError(f"{field_name} must not be empty.")
        try:
            number = int(text)
        except ValueError as exc:
            raise ValidationError(
                f"{field_name} must be an integer."
            ) from exc
        if number <= 0:
            raise ValidationError(f"{field_name} must be positive.")
        return number

    def _optional_text(self, value: str) -> str | None:
        text = value.strip()
        return text or None
