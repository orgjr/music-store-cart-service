from decimal import Decimal
from uuid import UUID, uuid4

from django.db import models


class Cart(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    customer = models.UUIDField(unique=True, blank=True, null=True)
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
