import uuid
from decimal import Decimal

from django.db import models

from .constants import (
    BALANCE_LENGTH, DECIMAL_LENGTH, DECIMAL_DEFAULT
)


class Wallet(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        verbose_name='Идентификатор'
    )
    balance = models.DecimalField(
        max_digits=BALANCE_LENGTH,
        decimal_places=DECIMAL_LENGTH,
        default=Decimal(DECIMAL_DEFAULT),
        verbose_name='Баланс'
    )

    class Meta:
        verbose_name='Кошелек'
        verbose_name_plural = 'Кошельки'
