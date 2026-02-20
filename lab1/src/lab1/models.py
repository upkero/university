from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, Optional


ID_PREFIXES = {
    "vendor": "V",
    "stall": "ST",
    "product": "P",
    "sale": "SL",
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
class Stall:
    stall_id: str
    name: str
    fee: Decimal
    vendor_id: Optional[str] = None

    def to_dict(self) -> dict[str, object]:
        return {
            "stall_id": self.stall_id,
            "name": self.name,
            "fee": str(self.fee),
            "vendor_id": self.vendor_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Stall":
        vendor_id = data.get("vendor_id")
        return cls(
            stall_id=str(data["stall_id"]),
            name=str(data["name"]),
            fee=Decimal(str(data["fee"])),
            vendor_id=str(vendor_id) if vendor_id is not None else None,
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
class Sale:
    sale_id: str
    product_id: str
    vendor_id: str
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
    stalls: Dict[str, Stall] = field(default_factory=dict)
    products: Dict[str, Product] = field(default_factory=dict)
    sales: Dict[str, Sale] = field(default_factory=dict)
    counters: Dict[str, int] = field(default_factory=dict)

    @classmethod
    def default(cls) -> "FairData":
        return cls(
            fair=Fair(
                name="Unnamed Fair",
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
            "stalls": {key: value.to_dict() for key, value in self.stalls.items()},
            "products": {
                key: value.to_dict() for key, value in self.products.items()
            },
            "sales": {key: value.to_dict() for key, value in self.sales.items()},
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
            counters={
                key: int(value)
                for key, value in dict(data.get("counters", {})).items()
            },
        )
