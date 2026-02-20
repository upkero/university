from decimal import Decimal

import pytest

from lab1.errors import ValidationError
from lab1.models import FairData
from lab1.service import FairService


def make_service() -> FairService:
    data = FairData.default()
    service = FairService(data)
    service.init_fair("Test Fair", "Test City", Decimal("5.00"))
    return service


def test_assign_stall_to_vendor() -> None:
    service = make_service()
    vendor = service.create_vendor("Alice")
    stall = service.create_stall("Main Hall", Decimal("10.00"))
    service.assign_stall(stall.stall_id, vendor.vendor_id)
    assert stall.vendor_id == vendor.vendor_id
    assert stall.stall_id in vendor.stall_ids


def test_sale_updates_balances_and_stock() -> None:
    service = make_service()
    vendor = service.create_vendor("Bob")
    product = service.add_product(
        vendor.vendor_id, "Apple", Decimal("2.50"), 10
    )
    sale = service.sell(product.product_id, 4, "Customer")
    assert product.quantity == 6
    assert sale.total == Decimal("10.00")
    assert sale.commission == Decimal("0.50")
    assert vendor.balance == Decimal("9.50")
    assert service.data.fair.balance == Decimal("0.50")


def test_sell_with_insufficient_stock_raises() -> None:
    service = make_service()
    vendor = service.create_vendor("Cara")
    product = service.add_product(
        vendor.vendor_id, "Bread", Decimal("1.00"), 1
    )
    with pytest.raises(ValidationError):
        service.sell(product.product_id, 2, "Customer")
