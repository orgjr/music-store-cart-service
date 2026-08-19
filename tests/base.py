from unittest import mock
from uuid import uuid4


def product_uuid(n):
    """Deterministic UUID derived from an integer, for stable test fixtures."""
    return f"00000000-0000-0000-0000-{n:012d}"


class ProductServiceMockMixin:
    """Patches the catalog HTTP call made by CartItemService.add_or_increase_quantity."""

    def setUp(self):
        super().setUp()
        self.products = {}
        patcher = mock.patch(
            "services.cart_item_service.requests.get",
            side_effect=self._product_service_get,
        )
        self.mock_get = patcher.start()
        self.addCleanup(patcher.stop)

    def _product_service_get(self, url, timeout=5):
        slug = url.rsplit("/", 1)[-1]
        response = mock.Mock()
        response.json.return_value = self.products.get(slug, {})
        return response

    def register_product(self, slug, name=None, price="1250.00", product_id=None):
        product = {
            "uuid": str(product_id) if product_id else str(uuid4()),
            "name": name or slug.replace("-", " ").title(),
            "slug": slug,
            "price": str(price),
            "image_url": f"https://cdn.example.com/img/{slug}.jpg",
        }
        self.products[slug] = product
        return product
