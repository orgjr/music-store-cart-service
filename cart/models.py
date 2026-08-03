from decimal import Decimal
from typing import ClassVar
from uuid import UUID, uuid4

from django.core.validators import MinValueValidator
from django.db import models


class Cart(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    customer = models.UUIDField(editable=False, unique=True, blank=True, null=True)
    price = models.DecimalField(
        decimal_places=2, max_digits=10, default=Decimal("0.00")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"customer: {self.customer}, cart: {self.uuid}"

    def clean(self):
        if not isinstance(self.uuid, UUID):
            self.uuid = uuid4()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product_id = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
    product_name = models.CharField(max_length=100)
    product_slug = models.SlugField(max_length=100)
    unit_price = models.DecimalField(decimal_places=2, max_digits=10)
    image_url = models.CharField(max_length=250)
    quantity = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)

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
