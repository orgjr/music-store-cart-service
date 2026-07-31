# Music Store Cart Service

API for managing the shopping cart of a music store, built with Django and Django REST Framework.

> Status: under active development. The application is not complete yet. The next releases will deliver all cart API endpoints, complete OpenAPI documentation, Docker/Docker Compose support, and expanded automated tests.

## Current capabilities

- Core API endpoints:
  - `GET /api/v1/` — returns application metadata, including the project name, version, description, environment, and links to the Redoc and health-check endpoints.
  - `GET /api/v1/health/` — returns the service status, ISO 8601 timestamp, and process uptime.
  - `GET /api/v1/schema/` — exposes the OpenAPI schema.
  - `GET /api/v1/docs/` — provides the Swagger UI documentation interface.
  - `GET /api/v1/redoc/` — provides the Redoc documentation interface.
- Cart domain services:
  - `CartService` — creates/retrieves carts, updates cart totals, and clears cart contents.
  - `CartItemService` — adds, removes, and updates item quantities, recalculating the cart total automatically.
- Automated tests: 24 tests covering the cart services.
- Environment-based configuration: separate settings for `base`, `dev`, `prod`, and `test`.

## Tech stack

- Python 3
- Django 6
- Django REST Framework
- django-environ (environment variables)
- drf-spectacular (OpenAPI, Swagger, and Redoc)
- ruff (linter)

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

## Project structure

```text
.
├── cart/
│   ├── migrations/
│   ├── services/
│   │   ├── cart_service.py
│   │   └── cart_item_service.py
│   ├── models.py
│   ├── tests.py
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
│   ├── tests.py
│   ├── urls.py
│   └── views.py
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

Note: the cart domain already has model and service logic implemented, but the public cart endpoints are not exposed yet. Those routes will be introduced in the next deliveries.

## Planned next deliveries

The following items are the main priorities for upcoming releases and will be emphasized in the next iterations:

- Delivery of the complete cart API endpoints for creating, reading, updating, and deleting cart items.
- Full OpenAPI documentation for the cart flows and request/response payloads.
- Docker and Docker Compose support for local and production environments.
- Expanded automated test coverage, including API and integration tests.
- Additional improvements around validation, error handling, and API consistency.
