from decimal import Decimal

from rest_framework import serializers

from .constants import (
    BALANCE_LENGTH, CHANGE_CHOICES,
    DECIMAL_LENGTH, MIN_CHANGE
)
from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'balance']


class ChangeBalanceSerializer(serializers.Serializer):
    operationType =serializers.ChoiceField(
        choices=CHANGE_CHOICES
    )
    amount = serializers.DecimalField(
        max_digits=BALANCE_LENGTH,
        decimal_places=DECIMAL_LENGTH,
        min_value=MIN_CHANGE
    )
