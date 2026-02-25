from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

from .errors import ConflictError, NotFoundError, ValidationError
from .models import (
    Attraction,
    Buyer,
    Fair,
    FairData,
    Product,
    Promotion,
    Sale,
    Stall,
    Vendor,
    Venue,
)

MONEY_PLACES = Decimal("0.01")
HUNDRED = Decimal("100")


def quantize_money(amount: Decimal) -> Decimal:
    return amount.quantize(MONEY_PLACES, rounding=ROUND_HALF_UP)


def ensure_name(value: str, field: str) -> str:
    name = value.strip()
    if not name:
        raise ValidationError(f"{field} must not be empty.")
    return name


def ensure_positive_int(value: int, field: str) -> int:
    if value <= 0:
        raise ValidationError(f"{field} must be a positive integer.")
    return value


def ensure_non_negative_money(value: Decimal, field: str) -> Decimal:
    if value < 0:
        raise ValidationError(f"{field} must be non-negative.")
    return quantize_money(value)


def ensure_positive_money(value: Decimal, field: str) -> Decimal:
    if value <= 0:
        raise ValidationError(f"{field} must be greater than zero.")
    return quantize_money(value)


def ensure_percent(value: Decimal, field: str) -> Decimal:
    value = quantize_money(value)
    if value < 0 or value > 100:
        raise ValidationError(f"{field} must be between 0 and 100.")
    return value


class FairService:
    def __init__(self, data: FairData) -> None:
        self.data = data

    def init_fair(self, name: str, location: str, commission_rate: Decimal) -> Fair:
        fair_name = ensure_name(name, "Fair name")
        fair_location = location.strip() or "Unknown"
        rate = ensure_percent(commission_rate, "Commission rate")
        self.data.fair = Fair(
            name=fair_name,
            location=fair_location,
            commission_rate=rate,
            balance=quantize_money(self.data.fair.balance),
        )
        return self.data.fair

    def create_venue(self, name: str, location: str) -> Venue:
        venue_name = ensure_name(name, "Venue name")
        venue_location = location.strip() or "Unknown"
        venue_id = self.data.next_id("venue")
        venue = Venue(
            venue_id=venue_id,
            name=venue_name,
            location=venue_location,
        )
        self.data.venues[venue_id] = venue
        return venue

    def create_vendor(self, name: str) -> Vendor:
        vendor_name = ensure_name(name, "Vendor name")
        vendor_id = self.data.next_id("vendor")
        vendor = Vendor(
            vendor_id=vendor_id,
            name=vendor_name,
            balance=Decimal("0.00"),
        )
        self.data.vendors[vendor_id] = vendor
        return vendor

    def create_buyer(self, name: str) -> Buyer:
        buyer_name = ensure_name(name, "Buyer name")
        buyer_id = self.data.next_id("buyer")
        buyer = Buyer(buyer_id=buyer_id, name=buyer_name)
        self.data.buyers[buyer_id] = buyer
        return buyer

    def create_stall(
        self, name: str, fee: Decimal, venue_id: str | None = None
    ) -> Stall:
        stall_name = ensure_name(name, "Stall name")
        stall_fee = ensure_non_negative_money(fee, "Stall fee")
        resolved_venue_id = None
        if venue_id:
            venue = self._get_venue(venue_id)
            resolved_venue_id = venue.venue_id
        stall_id = self.data.next_id("stall")
        stall = Stall(
            stall_id=stall_id,
            name=stall_name,
            fee=stall_fee,
            venue_id=resolved_venue_id,
        )
        self.data.stalls[stall_id] = stall
        return stall

    def assign_stall(self, stall_id: str, vendor_id: str) -> Stall:
        stall = self._get_stall(stall_id)
        if stall.vendor_id is not None:
            raise ConflictError("Stall is already assigned.")
        vendor = self._get_vendor(vendor_id)
        stall.vendor_id = vendor.vendor_id
        if stall.stall_id not in vendor.stall_ids:
            vendor.stall_ids.append(stall.stall_id)
        return stall

    def add_product(
        self, vendor_id: str, name: str, price: Decimal, quantity: int
    ) -> Product:
        vendor = self._get_vendor(vendor_id)
        product_name = ensure_name(name, "Product name")
        product_price = ensure_positive_money(price, "Product price")
        product_quantity = ensure_positive_int(quantity, "Product quantity")
        product_id = self.data.next_id("product")
        product = Product(
            product_id=product_id,
            vendor_id=vendor.vendor_id,
            name=product_name,
            price=product_price,
            quantity=product_quantity,
        )
        self.data.products[product_id] = product
        return product

    def trade(
        self,
        product_id: str,
        quantity: int,
        buyer: str | None = None,
        buyer_id: str | None = None,
        unit_price: Decimal | None = None,
    ) -> Sale:
        product = self._get_product(product_id)
        sale_quantity = ensure_positive_int(quantity, "Trade quantity")
        if product.quantity < sale_quantity:
            raise ValidationError("Insufficient stock for sale.")
        resolved_buyer_id = None
        buyer_name = (buyer or "").strip()
        if buyer_id:
            buyer_entity = self._get_buyer(buyer_id)
            buyer_name = buyer_entity.name
            resolved_buyer_id = buyer_entity.buyer_id
        if not buyer_name:
            buyer_name = "Anonymous"
        price = product.price
        if unit_price is not None:
            price = ensure_positive_money(unit_price, "Negotiated price")
        total = quantize_money(price * sale_quantity)
        commission = quantize_money(
            total * self.data.fair.commission_rate / HUNDRED
        )
        vendor = self._get_vendor(product.vendor_id)
        vendor.balance = quantize_money(vendor.balance + total - commission)
        self.data.fair.balance = quantize_money(self.data.fair.balance + commission)
        product.quantity -= sale_quantity
        sale_id = self.data.next_id("sale")
        timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        sale = Sale(
            sale_id=sale_id,
            product_id=product.product_id,
            vendor_id=product.vendor_id,
            buyer_id=resolved_buyer_id,
            buyer=buyer_name,
            quantity=sale_quantity,
            unit_price=price,
            total=total,
            commission=commission,
            timestamp=timestamp,
        )
        self.data.sales[sale_id] = sale
        return sale

    def sell(self, product_id: str, quantity: int, buyer: str) -> Sale:
        return self.trade(product_id, quantity, buyer=buyer)

    def load_goods(self, product_id: str, quantity: int) -> Product:
        product = self._get_product(product_id)
        load_quantity = ensure_positive_int(quantity, "Load quantity")
        product.quantity += load_quantity
        return product

    def unload_goods(self, product_id: str, quantity: int) -> Product:
        product = self._get_product(product_id)
        unload_quantity = ensure_positive_int(quantity, "Unload quantity")
        if product.quantity < unload_quantity:
            raise ValidationError("Insufficient stock to unload.")
        product.quantity -= unload_quantity
        return product

    def advertise_event(self, message: str) -> Promotion:
        promotion_message = ensure_name(message, "Promotion message")
        promotion_id = self.data.next_id("promotion")
        timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        promotion = Promotion(
            promotion_id=promotion_id,
            message=promotion_message,
            timestamp=timestamp,
        )
        self.data.promotions[promotion_id] = promotion
        return promotion

    def add_attraction(
        self, name: str, description: str = "", venue_id: str | None = None
    ) -> Attraction:
        attraction_name = ensure_name(name, "Attraction name")
        resolved_venue_id = None
        if venue_id:
            venue = self._get_venue(venue_id)
            resolved_venue_id = venue.venue_id
        attraction_id = self.data.next_id("attraction")
        attraction = Attraction(
            attraction_id=attraction_id,
            name=attraction_name,
            description=description.strip(),
            venue_id=resolved_venue_id,
        )
        self.data.attractions[attraction_id] = attraction
        return attraction

    def list_vendors(self) -> list[Vendor]:
        return sorted(self.data.vendors.values(), key=lambda item: item.vendor_id)

    def list_buyers(self) -> list[Buyer]:
        return sorted(self.data.buyers.values(), key=lambda item: item.buyer_id)

    def list_venues(self) -> list[Venue]:
        return sorted(self.data.venues.values(), key=lambda item: item.venue_id)

    def list_stalls(self) -> list[Stall]:
        return sorted(self.data.stalls.values(), key=lambda item: item.stall_id)

    def list_products(self) -> list[Product]:
        return sorted(self.data.products.values(), key=lambda item: item.product_id)

    def list_sales(self) -> list[Sale]:
        return sorted(self.data.sales.values(), key=lambda item: item.sale_id)

    def list_promotions(self) -> list[Promotion]:
        return sorted(
            self.data.promotions.values(), key=lambda item: item.promotion_id
        )

    def list_attractions(self) -> list[Attraction]:
        return sorted(
            self.data.attractions.values(), key=lambda item: item.attraction_id
        )

    def summary(self) -> dict[str, Decimal | int]:
        total_sales = sum(
            (sale.total for sale in self.data.sales.values()), Decimal("0.00")
        )
        total_commission = sum(
            (sale.commission for sale in self.data.sales.values()), Decimal("0.00")
        )
        return {
            "vendors": len(self.data.vendors),
            "buyers": len(self.data.buyers),
            "venues": len(self.data.venues),
            "stalls": len(self.data.stalls),
            "products": len(self.data.products),
            "sales": len(self.data.sales),
            "promotions": len(self.data.promotions),
            "attractions": len(self.data.attractions),
            "total_sales": quantize_money(total_sales),
            "total_commission": quantize_money(total_commission),
            "fair_balance": quantize_money(self.data.fair.balance),
        }

    def vendor_report(self, vendor_id: str) -> dict[str, Decimal | int | str]:
        vendor = self._get_vendor(vendor_id)
        sales = [
            sale for sale in self.data.sales.values() if sale.vendor_id == vendor_id
        ]
        total_sales = sum((sale.total for sale in sales), Decimal("0.00"))
        return {
            "vendor_id": vendor.vendor_id,
            "name": vendor.name,
            "balance": quantize_money(vendor.balance),
            "sales_count": len(sales),
            "total_sales": quantize_money(total_sales),
            "products_count": len(
                [
                    product
                    for product in self.data.products.values()
                    if product.vendor_id == vendor_id
                ]
            ),
            "stalls_count": len(vendor.stall_ids),
        }

    def _get_vendor(self, vendor_id: str) -> Vendor:
        vendor = self.data.vendors.get(vendor_id)
        if vendor is None:
            raise NotFoundError(f"Vendor '{vendor_id}' not found.")
        return vendor

    def _get_buyer(self, buyer_id: str) -> Buyer:
        buyer = self.data.buyers.get(buyer_id)
        if buyer is None:
            raise NotFoundError(f"Buyer '{buyer_id}' not found.")
        return buyer

    def _get_venue(self, venue_id: str) -> Venue:
        venue = self.data.venues.get(venue_id)
        if venue is None:
            raise NotFoundError(f"Venue '{venue_id}' not found.")
        return venue

    def _get_stall(self, stall_id: str) -> Stall:
        stall = self.data.stalls.get(stall_id)
        if stall is None:
            raise NotFoundError(f"Stall '{stall_id}' not found.")
        return stall

    def _get_product(self, product_id: str) -> Product:
        product = self.data.products.get(product_id)
        if product is None:
            raise NotFoundError(f"Product '{product_id}' not found.")
        return product
