"""Shared OpenAPI documentation config for the cart app."""

TAGS = ["Cart"]
ITEM_TAGS = ["Cart Item"]

NOT_FOUND_SCHEMA = {
    "type": "object",
    "properties": {"detail": {"type": "string"}},
}

VALIDATION_ERROR_SCHEMA = {
    "type": "object",
    "additionalProperties": {"type": "array", "items": {"type": "string"}},
}

ITEM_EXAMPLE = {
    "uuid": "8c9a1f3b-4d2e-4a7b-9c5f-1e6d2a8b4c0d",
    "cart": "b7a2e5f1-8c4d-4f0e-9a1b-3c6d8e0f2a1b",
    "product_id": "0d3a2f1c-6b8e-4f5a-9d7c-2a1b3c4d5e6f",
    "product_name": "Fender Stratocaster",
    "product_slug": "fender-stratocaster",
    "product_price": "1250.00",
    "quantity": 1,
    "price": "1250.00",
    "added_at": "2026-08-03T17:00:00Z",
    "updated_at": "2026-08-03T17:00:00Z",
    "image_url": "https://cdn.example.com/img/fender-stratocaster.jpg",
}

CART_EXAMPLE = {
    "uuid": "b7a2e5f1-8c4d-4f0e-9a1b-3c6d8e0f2a1b",
    "customer": None,
    "price": "2500.00",
    "items": [{**ITEM_EXAMPLE, "quantity": 2, "price": "2500.00"}],
    "created_at": "2026-08-03T17:00:00Z",
    "updated_at": "2026-08-03T17:00:00Z",
}

CUSTOMER_UUID = "3f2a9c1d-5e6b-4f8a-9b2c-7d1e0f3a4b5c"

CUSTOMER_CART_EXAMPLE = {**CART_EXAMPLE, "customer": CUSTOMER_UUID}

CART_CREATE_PAYLOAD_EXAMPLE = {"customer": CUSTOMER_UUID}

EMPTY_CART_EXAMPLE = {
    "uuid": "b7a2e5f1-8c4d-4f0e-9a1b-3c6d8e0f2a1b",
    "customer": None,
    "price": "0.00",
    "items": [],
    "created_at": "2026-08-03T17:00:00Z",
    "updated_at": "2026-08-03T17:00:00Z",
}

ITEM_PAYLOAD_EXAMPLE = {
    "cart": "b7a2e5f1-8c4d-4f0e-9a1b-3c6d8e0f2a1b",
    "product_slug": "fender-stratocaster",
    "quantity": 1,
}

ITEM_UPDATE_PAYLOAD_EXAMPLE = {
    **ITEM_PAYLOAD_EXAMPLE,
    "quantity": 3,
}

CART_LIST_EXAMPLE = CART_EXAMPLE

ITEM_LIST_EXAMPLE = ITEM_EXAMPLE
