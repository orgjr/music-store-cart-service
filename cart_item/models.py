from decimal import Decimal
from typing import ClassVar
from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models

from cart.models import Cart


class CartItem(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product_id = models.UUIDField(editable=False)
    product_name = models.CharField(max_length=100)
    product_slug = models.SlugField(max_length=100)
    product_price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["cart", "product_id"], name="one_product_per_cart"
            )
        ]
