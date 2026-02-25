from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, Optional


ID_PREFIXES = {
    "vendor": "V",
    "buyer": "B",
    "venue": "VN",
    "stall": "ST",
    "product": "P",
    "sale": "SL",
    "promotion": "PR",
    "attraction": "AT",
}


@dataclass
class Fair:
    name: str
    location: str
    commission_rate: Decimal
    balance: Decimal

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "location": self.location,
            "commission_rate": str(self.commission_rate),
            "balance": str(self.balance),
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Fair":
        return cls(
            name=data["name"],
            location=data["location"],
            commission_rate=Decimal(data["commission_rate"]),
            balance=Decimal(data["balance"]),
        )


@dataclass
class Venue:
    venue_id: str
    name: str
    location: str

    def to_dict(self) -> dict[str, str]:
        return {
            "venue_id": self.venue_id,
            "name": self.name,
            "location": self.location,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Venue":
        return cls(
            venue_id=str(data["venue_id"]),
            name=str(data["name"]),
            location=str(data["location"]),
        )


@dataclass
class Vendor:
    vendor_id: str
    name: str
    balance: Decimal
    stall_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "vendor_id": self.vendor_id,
            "name": self.name,
            "balance": str(self.balance),
            "stall_ids": list(self.stall_ids),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Vendor":
        return cls(
            vendor_id=str(data["vendor_id"]),
            name=str(data["name"]),
            balance=Decimal(str(data["balance"])),
            stall_ids=[str(item) for item in data.get("stall_ids", [])],
        )


@dataclass
class Buyer:
    buyer_id: str
    name: str

    def to_dict(self) -> dict[str, str]:
        return {
            "buyer_id": self.buyer_id,
            "name": self.name,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Buyer":
        return cls(
            buyer_id=str(data["buyer_id"]),
            name=str(data["name"]),
        )


@dataclass
class Stall:
    stall_id: str
    name: str
    fee: Decimal
    vendor_id: Optional[str] = None
    venue_id: Optional[str] = None

    def to_dict(self) -> dict[str, object]:
        return {
            "stall_id": self.stall_id,
            "name": self.name,
            "fee": str(self.fee),
            "vendor_id": self.vendor_id,
            "venue_id": self.venue_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Stall":
        vendor_id = data.get("vendor_id")
        venue_id = data.get("venue_id")
        return cls(
            stall_id=str(data["stall_id"]),
            name=str(data["name"]),
            fee=Decimal(str(data["fee"])),
            vendor_id=str(vendor_id) if vendor_id is not None else None,
            venue_id=str(venue_id) if venue_id is not None else None,
        )


@dataclass
class Product:
    product_id: str
    vendor_id: str
    name: str
    price: Decimal
    quantity: int

    def to_dict(self) -> dict[str, object]:
        return {
            "product_id": self.product_id,
            "vendor_id": self.vendor_id,
            "name": self.name,
            "price": str(self.price),
            "quantity": self.quantity,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Product":
        return cls(
            product_id=str(data["product_id"]),
            vendor_id=str(data["vendor_id"]),
            name=str(data["name"]),
            price=Decimal(str(data["price"])),
            quantity=int(data["quantity"]),
        )


@dataclass
class Promotion:
    promotion_id: str
    message: str
    timestamp: str

    def to_dict(self) -> dict[str, str]:
        return {
            "promotion_id": self.promotion_id,
            "message": self.message,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Promotion":
        return cls(
            promotion_id=str(data["promotion_id"]),
            message=str(data["message"]),
            timestamp=str(data["timestamp"]),
        )


@dataclass
class Attraction:
    attraction_id: str
    name: str
    description: str
    venue_id: Optional[str] = None

    def to_dict(self) -> dict[str, object]:
        return {
            "attraction_id": self.attraction_id,
            "name": self.name,
            "description": self.description,
            "venue_id": self.venue_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Attraction":
        venue_id = data.get("venue_id")
        return cls(
            attraction_id=str(data["attraction_id"]),
            name=str(data["name"]),
            description=str(data.get("description", "")),
            venue_id=str(venue_id) if venue_id is not None else None,
        )


@dataclass
class Sale:
    sale_id: str
    product_id: str
    vendor_id: str
    buyer_id: Optional[str]
    buyer: str
    quantity: int
    unit_price: Decimal
    total: Decimal
    commission: Decimal
    timestamp: str

    def to_dict(self) -> dict[str, object]:
        return {
            "sale_id": self.sale_id,
            "product_id": self.product_id,
            "vendor_id": self.vendor_id,
            "buyer_id": self.buyer_id,
            "buyer": self.buyer,
            "quantity": self.quantity,
            "unit_price": str(self.unit_price),
            "total": str(self.total),
            "commission": str(self.commission),
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Sale":
        return cls(
            sale_id=str(data["sale_id"]),
            product_id=str(data["product_id"]),
            vendor_id=str(data["vendor_id"]),
            buyer_id=str(data["buyer_id"])
            if data.get("buyer_id") is not None
            else None,
            buyer=str(data["buyer"]),
            quantity=int(data["quantity"]),
            unit_price=Decimal(str(data["unit_price"])),
            total=Decimal(str(data["total"])),
            commission=Decimal(str(data["commission"])),
            timestamp=str(data["timestamp"]),
        )


@dataclass
class FairData:
    fair: Fair
    vendors: Dict[str, Vendor] = field(default_factory=dict)
    buyers: Dict[str, Buyer] = field(default_factory=dict)
    venues: Dict[str, Venue] = field(default_factory=dict)
    stalls: Dict[str, Stall] = field(default_factory=dict)
    products: Dict[str, Product] = field(default_factory=dict)
    sales: Dict[str, Sale] = field(default_factory=dict)
    promotions: Dict[str, Promotion] = field(default_factory=dict)
    attractions: Dict[str, Attraction] = field(default_factory=dict)
    counters: Dict[str, int] = field(default_factory=dict)

    @classmethod
    def default(cls) -> "FairData":
        return cls(
            fair=Fair(
                name="Unnamed Market",
                location="Unknown",
                commission_rate=Decimal("0.00"),
                balance=Decimal("0.00"),
            )
        )

    def next_id(self, kind: str) -> str:
        if kind not in ID_PREFIXES:
            raise ValueError(f"Unknown id kind: {kind}")
        current = self.counters.get(kind, 0) + 1
        self.counters[kind] = current
        prefix = ID_PREFIXES[kind]
        return f"{prefix}{current:04d}"

    def to_dict(self) -> dict[str, object]:
        return {
            "fair": self.fair.to_dict(),
            "vendors": {key: value.to_dict() for key, value in self.vendors.items()},
            "buyers": {key: value.to_dict() for key, value in self.buyers.items()},
            "venues": {key: value.to_dict() for key, value in self.venues.items()},
            "stalls": {key: value.to_dict() for key, value in self.stalls.items()},
            "products": {
                key: value.to_dict() for key, value in self.products.items()
            },
            "sales": {key: value.to_dict() for key, value in self.sales.items()},
            "promotions": {
                key: value.to_dict() for key, value in self.promotions.items()
            },
            "attractions": {
                key: value.to_dict() for key, value in self.attractions.items()
            },
            "counters": dict(self.counters),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FairData":
        return cls(
            fair=Fair.from_dict(data["fair"]),
            vendors={
                key: Vendor.from_dict(value)
                for key, value in dict(data.get("vendors", {})).items()
            },
            buyers={
                key: Buyer.from_dict(value)
                for key, value in dict(data.get("buyers", {})).items()
            },
            venues={
                key: Venue.from_dict(value)
                for key, value in dict(data.get("venues", {})).items()
            },
            stalls={
                key: Stall.from_dict(value)
                for key, value in dict(data.get("stalls", {})).items()
            },
            products={
                key: Product.from_dict(value)
                for key, value in dict(data.get("products", {})).items()
            },
            sales={
                key: Sale.from_dict(value)
                for key, value in dict(data.get("sales", {})).items()
            },
            promotions={
                key: Promotion.from_dict(value)
                for key, value in dict(data.get("promotions", {})).items()
            },
            attractions={
                key: Attraction.from_dict(value)
                for key, value in dict(data.get("attractions", {})).items()
            },
            counters={
                key: int(value)
                for key, value in dict(data.get("counters", {})).items()
            },
        )
