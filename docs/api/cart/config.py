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
    "id": 1,
    "cart": "b7a2e5f1-8c4d-4f0e-9a1b-3c6d8e0f2a1b",
    "product_id": 10,
    "product_name": "Fender Stratocaster",
    "product_slug": "fender-stratocaster",
    "unit_price": "1250.00",
    "image_url": "https://cdn.example.com/img/fender-stratocaster.jpg",
    "quantity": 1,
    "added_at": "2026-08-03T17:00:00Z",
}

CART_EXAMPLE = {
    "uuid": "b7a2e5f1-8c4d-4f0e-9a1b-3c6d8e0f2a1b",
    "customer": None,
    "price": "2500.00",
    "items": [{**ITEM_EXAMPLE, "quantity": 2}],
    "created_at": "2026-08-03T17:00:00Z",
    "updated_at": "2026-08-03T17:00:00Z",
}

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
    "product_id": 10,
    "product_name": "Fender Stratocaster",
    "product_slug": "fender-stratocaster",
    "unit_price": "1250.00",
    "image_url": "https://cdn.example.com/img/fender-stratocaster.jpg",
    "quantity": 1,
}

ITEM_UPDATE_PAYLOAD_EXAMPLE = {
    **ITEM_PAYLOAD_EXAMPLE,
    "quantity": 3,
}

CART_LIST_EXAMPLE = CART_EXAMPLE

ITEM_LIST_EXAMPLE = ITEM_EXAMPLE
