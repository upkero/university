from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import TypeVar

from .models import (
    Attraction,
    Buyer,
    Fair,
    Product,
    Promotion,
    Sale,
    Stall,
    Vendor,
    Venue,
)
from .service import FairService
from .storage import DataStore

T = TypeVar("T")


class FairApplication:
    """Shared application layer for CLI and GUI clients."""

    def __init__(self, store: DataStore) -> None:
        self._store = store
        self._data = store.load()
        self._service = FairService(self._data)

    @classmethod
    def from_path(cls, data_path: Path) -> "FairApplication":
        return cls(DataStore(data_path))

    @property
    def fair(self) -> Fair:
        return self._data.fair

    def init_fair(
        self, name: str, location: str, commission_rate: Decimal
    ) -> Fair:
        return self._commit(
            self._service.init_fair(name, location, commission_rate)
        )

    def create_venue(self, name: str, location: str) -> Venue:
        return self._commit(self._service.create_venue(name, location))

    def create_vendor(self, name: str) -> Vendor:
        return self._commit(self._service.create_vendor(name))

    def create_buyer(self, name: str) -> Buyer:
        return self._commit(self._service.create_buyer(name))

    def create_stall(
        self, name: str, fee: Decimal, venue_id: str | None = None
    ) -> Stall:
        return self._commit(self._service.create_stall(name, fee, venue_id))

    def assign_stall(self, stall_id: str, vendor_id: str) -> Stall:
        return self._commit(self._service.assign_stall(stall_id, vendor_id))

    def add_product(
        self,
        vendor_id: str,
        name: str,
        price: Decimal,
        quantity: int,
    ) -> Product:
        return self._commit(
            self._service.add_product(vendor_id, name, price, quantity)
        )

    def sell(self, product_id: str, quantity: int, buyer: str) -> Sale:
        return self._commit(self._service.sell(product_id, quantity, buyer))

    def trade(
        self,
        product_id: str,
        quantity: int,
        buyer: str | None = None,
        buyer_id: str | None = None,
        unit_price: Decimal | None = None,
    ) -> Sale:
        return self._commit(
            self._service.trade(
                product_id,
                quantity,
                buyer=buyer,
                buyer_id=buyer_id,
                unit_price=unit_price,
            )
        )

    def load_goods(self, product_id: str, quantity: int) -> Product:
        return self._commit(self._service.load_goods(product_id, quantity))

    def unload_goods(self, product_id: str, quantity: int) -> Product:
        return self._commit(self._service.unload_goods(product_id, quantity))

    def advertise_event(self, message: str) -> Promotion:
        return self._commit(self._service.advertise_event(message))

    def add_attraction(
        self, name: str, description: str = "", venue_id: str | None = None
    ) -> Attraction:
        return self._commit(
            self._service.add_attraction(name, description, venue_id)
        )

    def list_vendors(self) -> list[Vendor]:
        return self._service.list_vendors()

    def list_buyers(self) -> list[Buyer]:
        return self._service.list_buyers()

    def list_venues(self) -> list[Venue]:
        return self._service.list_venues()

    def list_stalls(self) -> list[Stall]:
        return self._service.list_stalls()

    def list_products(self) -> list[Product]:
        return self._service.list_products()

    def list_sales(self) -> list[Sale]:
        return self._service.list_sales()

    def list_promotions(self) -> list[Promotion]:
        return self._service.list_promotions()

    def list_attractions(self) -> list[Attraction]:
        return self._service.list_attractions()

    def summary(self) -> dict[str, Decimal | int]:
        return self._service.summary()

    def vendor_report(
        self, vendor_id: str
    ) -> dict[str, Decimal | int | str]:
        return self._service.vendor_report(vendor_id)

    def _commit(self, result: T) -> T:
        self._store.save(self._data)
        return result
