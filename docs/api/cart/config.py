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

CART_EXAMPLE = {
    "uuid": "b7a2e5f1-8c4d-4f0e-9a1b-3c6d8e0f2a1b",
    "customer": None,
    "price": "1250.00",
    "items": [
        {
            "id": 1,
            "cart": "b7a2e5f1-8c4d-4f0e-9a1b-3c6d8e0f2a1b",
            "product_id": 10,
            "product_name": "Fender Stratocaster",
            "product_slug": "fender-stratocaster",
            "unit_price": "1250.00",
            "image_url": "https://cdn.example.com/img/fender-stratocaster.jpg",
            "quantity": 1,
            "added_at": "2026-08-03T14:00:00-03:00",
        }
    ],
    "created_at": "2026-08-03T14:00:00-03:00",
    "updated_at": "2026-08-03T14:00:00-03:00",
}

ITEM_EXAMPLE = CART_EXAMPLE["items"][0]

ITEM_PAYLOAD_EXAMPLE = {
    "cart": "b7a2e5f1-8c4d-4f0e-9a1b-3c6d8e0f2a1b",
    "product_id": 10,
    "product_name": "Fender Stratocaster",
    "product_slug": "fender-stratocaster",
    "unit_price": "1250.00",
    "image_url": "https://cdn.example.com/img/fender-stratocaster.jpg",
    "quantity": 1,
}
