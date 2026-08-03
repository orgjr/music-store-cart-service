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
- Complete cart API endpoints: creation, retrieval, update, and deletion of carts and cart items, plus quantity increment/decrement and cart clearing.
- Cart domain services:
  - `CartService` — creates/retrieves carts, updates cart totals, and clears cart contents.
  - `CartItemService` — adds, removes, and updates item quantities, recalculating the cart total automatically.
- Full OpenAPI documentation in English, organized per endpoint group (`Index`, `Health`, `Cart`, `Cart Item`) with request/response examples and error examples.
- Docker and Docker Compose support for local development.
- Automated tests: 110 tests covering domain services, models, API functionality, and app-level smoke and functional flows.
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
- Copy `.env.example` to `.env` and adjust the values, especially `SECRET_KEY`:

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
│   ├── services/
│   │   ├── cart_service.py
│   │   └── cart_item_service.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
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
- `POST /api/v1/cart/` — creates (or reuses) a cart.
- `GET /api/v1/cart/` — lists carts (paginated).
- `GET /api/v1/cart/{uuid}/` — retrieves a cart with its items.
- `PUT /api/v1/cart/{uuid}/` — updates a cart.
- `PATCH /api/v1/cart/{uuid}/` — partially updates a cart.
- `DELETE /api/v1/cart/{uuid}/` — deletes a cart.
- `DELETE /api/v1/cart/{uuid}/items/` — clears all items from a cart.
- `GET /api/v1/cart/items/` — lists cart items (paginated).
- `POST /api/v1/cart/items/` — adds an item to a cart; if the product already exists, its quantity is summed.
- `GET /api/v1/cart/items/{id}/` — retrieves a cart item.
- `PUT /api/v1/cart/items/{id}/` — updates a cart item.
- `PATCH /api/v1/cart/items/{id}/` — partially updates a cart item; the quantity field is treated as a delta.
- `DELETE /api/v1/cart/items/{id}/` — removes an item from a cart.
- `POST /api/v1/cart/items/{id}/increment/` — increments the item quantity.
- `POST /api/v1/cart/items/{id}/decrement/` — decrements the item quantity; removes the item when it reaches zero.

## Next delivery

The following items are the priorities for the next iteration:

- Integrate all microservices across the platform.
- Deploy the complete platform locally with Docker.
- Implement smoke and integration tests.
