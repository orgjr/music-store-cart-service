# Music Store Cart Service

API for managing the shopping cart of a music store, built with Django and Django REST Framework.

> Status: all planned deliveries for this release are complete. The next delivery will integrate all services and add the Identity service, responsible for identity and authentication.

## Current capabilities

- Core API endpoints:
  - `GET /api/v1/` — returns application metadata, including the project name, version, description, environment, and links to the Redoc and health-check endpoints.
  - `GET /api/v1/health/` — returns the service status, ISO 8601 timestamp, and process uptime.
  - `GET /api/v1/schema/` — exposes the OpenAPI schema.
  - `GET /api/v1/docs/` — provides the Swagger UI documentation interface.
  - `GET /api/v1/redoc/` — provides the Redoc documentation interface.
- Complete cart API endpoints: creation, retrieval, and deletion of carts and cart items, plus quantity increment/decrement and cart clearing.
- Cart items are added by `product_slug`; product data (name, price, image) is resolved from the catalog service (`PRODUCT_SERVICE_URL`) instead of being sent by the client.
- Carts are tied to an optional customer UUID (one cart per customer); creating a cart with a known customer returns the existing cart.
- Dedicated `cart_item` app for the `CartItem` model (models, serializers, views, and routes), with its own migrations.
- Cart domain services (in the top-level `services/` package):
  - `CartService` — creates/retrieves carts by customer (one cart per customer), updates cart totals (including `updated_at`), and clears cart contents.
  - `CartItemService` — adds/increases item quantities, increments/decrements, sets quantities, and clears items, recalculating the cart total automatically.
- Full OpenAPI documentation in English, organized per endpoint group (`Index`, `Health`, `Cart`, `Cart Item`) with request/response examples and error examples.
- Docker and Docker Compose support for local development.
- Automated tests: 127 tests covering domain services, models, API functionality, and app-level smoke and functional flows.
- Environment-based configuration: separate settings for `base`, `dev`, `prod`, and `test`.

## Tech stack

- Python 3.13
- Django 6
- Django REST Framework
- django-environ (environment variables)
- drf-spectacular (OpenAPI, Swagger, and Redoc)
- ruff (linter)
- Docker and Docker Compose

## Running the project

### Prerequisites

- Python 3.x
- Copy `.env.example` to `.env` and adjust the values, especially `SECRET_KEY` and `PRODUCT_SERVICE_URL` (the catalog service used to resolve product data when adding items):

```bash
cp .env.example .env
```

### Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Tests

```bash
python manage.py test
```

### Lint

```bash
ruff check .
```

### Running with Docker

Prerequisite: a local `.env` file (see Prerequisites above).

```bash
docker compose up -d
```

The service starts at `http://localhost:8001/` and applies migrations automatically on startup.

## Project structure

```text
.
├── cart/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── cart_item/
│   ├── migrations/
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── services/
│   ├── cart_service.py
│   ├── cart_item_service.py
│   └── request_updated_product.py
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── prod.py
│   │   └── test.py
│   ├── api_v1_urls.py
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── helpers/
│   │   ├── build_url.py
│   │   └── uptime.py
│   ├── migrations/
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── docs/
│   └── api/
│       ├── cart/
│       └── core/
├── tests/
│   ├── base.py
│   ├── cart/
│   │   ├── test_models/
│   │   ├── test_services/
│   │   ├── test_endpoints/
│   │   └── test_functional/
│   └── core/
│       ├── test_smoke/
│       ├── test_endpoints/
│       └── test_functional/
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── manage.py
├── requirements.txt
└── README.md
```

## Current API endpoints

All API routes are versioned under `/api/v1/`.

- `GET /api/v1/` — returns application metadata and links to the documentation and health endpoints.
- `GET /api/v1/health/` — returns the service health status and uptime information.
- `GET /api/v1/schema/` — returns the OpenAPI schema.
- `GET /api/v1/docs/` — renders the Swagger UI documentation interface.
- `GET /api/v1/redoc/` — renders the Redoc documentation interface.
- `POST /api/v1/cart/` — creates a cart, optionally accepting `{"customer": "<uuid>"}` to create or reuse that customer's cart (one cart per customer).
- `GET /api/v1/cart/` — lists carts (paginated).
- `GET /api/v1/cart/{uuid}/` — retrieves a cart with its items.
- `DELETE /api/v1/cart/{uuid}/items/` — clears all items from a cart.
- `GET /api/v1/cart/items/` — lists cart items (paginated).
- `POST /api/v1/cart/items/` — adds an item to a cart by product slug; if the product already exists, its quantity is summed.
- `GET /api/v1/cart/items/{uuid}/` — retrieves a cart item.
- `PUT /api/v1/cart/items/{uuid}/` — updates a cart item.
- `PATCH /api/v1/cart/items/{uuid}/` — partially updates a cart item; the quantity field sets the item quantity directly.
- `DELETE /api/v1/cart/items/{uuid}/` — removes an item from a cart.
- `POST /api/v1/cart/items/{uuid}/increment/` — increments the item quantity.
- `POST /api/v1/cart/items/{uuid}/decrement/` — decrements the item quantity; removes the item when it reaches zero.

## Next delivery

The following items are the priorities for the next iteration:

- Integrate all microservices across the platform.
- Deploy the complete platform locally with Docker.
- Implement smoke and integration tests.
