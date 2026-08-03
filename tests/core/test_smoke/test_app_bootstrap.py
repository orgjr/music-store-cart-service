from django.apps import apps
from django.conf import settings
from django.test import SimpleTestCase

API_ROOT = "/api/v1"


class BootstrapSmokeTests(SimpleTestCase):
    def test_environment_is_test(self):
        self.assertEqual(settings.ENVIRONMENT, "test")

    def test_required_apps_are_installed(self):
        expected = ["core", "cart", "rest_framework", "drf_spectacular"]
        self.assertTrue(all(app in settings.INSTALLED_APPS for app in expected))

    def test_core_and_cart_app_configs_are_loaded(self):
        self.assertEqual(apps.get_app_config("core").name, "core")
        self.assertEqual(apps.get_app_config("cart").name, "cart")

    def test_api_root_prefix_is_v1(self):
        self.assertEqual(settings.API_ROOT_PREFIX, API_ROOT + "/")

    def test_spectacular_tags_cover_all_endpoint_tags(self):
        tag_names = {tag["name"] for tag in settings.SPECTACULAR_SETTINGS["TAGS"]}
        self.assertEqual(tag_names, {"Index", "Health", "Cart", "Cart Item"})