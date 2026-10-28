"""Unit tests for Pydantic sales / product / customer schemas."""
import pytest
from pydantic import ValidationError

from src.models.schemas import Sale, Product, Customer


def _valid_sale(**overrides):
    data = {
        "transaction_id": "txn-001",
        "customer_id": 10,
        "product_id": 5,
        "quantity": 2,
        "unit_price": 12.5,
        "total_amount": 25.0,
        "transaction_timestamp": "2024-07-15T10:00:00",
        "payment_method": "credit_card",
        "store_id": 1,
        "status": "completed",
    }
    data.update(overrides)
    return data


def test_sale_accepts_valid_record():
    sale = Sale(**_valid_sale())
    assert sale.transaction_id == "txn-001"
    assert sale.total_amount == 25.0


def test_sale_rejects_mismatched_total():
    with pytest.raises(ValidationError):
        Sale(**_valid_sale(total_amount=99.0))


def test_sale_rejects_invalid_payment_method():
    with pytest.raises(ValidationError):
        Sale(**_valid_sale(payment_method="bitcoin"))


def test_sale_rejects_invalid_status():
    with pytest.raises(ValidationError):
        Sale(**_valid_sale(status="refunded"))


def test_sale_rejects_non_positive_quantity():
    with pytest.raises(ValidationError):
        Sale(**_valid_sale(quantity=0, total_amount=0.0))


def test_product_accepts_valid_record():
    product = Product(
        product_id=1,
        product_name="Widget",
        category="Tools",
        base_price=9.99,
        stock_quantity=100,
    )
    assert product.product_name == "Widget"


def test_product_rejects_negative_stock():
    with pytest.raises(ValidationError):
        Product(
            product_id=1,
            product_name="Widget",
            category="Tools",
            base_price=9.99,
            stock_quantity=-1,
        )


def test_customer_accepts_valid_segment():
    customer = Customer(
        customer_id=1,
        customer_name="Ada Lovelace",
        email="ada@example.com",
        phone="+1-555-0100",
        city="London",
        country="UK",
        signup_date="2024-01-01",
        customer_segment="Premium",
    )
    assert customer.customer_segment == "Premium"


def test_customer_rejects_invalid_segment():
    with pytest.raises(ValidationError):
        Customer(
            customer_id=1,
            customer_name="Ada Lovelace",
            email="ada@example.com",
            phone="+1-555-0100",
            city="London",
            country="UK",
            signup_date="2024-01-01",
            customer_segment="VIP",
        )
