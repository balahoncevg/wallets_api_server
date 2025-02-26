from rest_framework import serializers

from .constants import (
    BALANCE_LENGTH, CHANGE_CHOICES,
    DECIMAL_LENGTH, MIN_CHANGE
)
from wallets.models import Wallet


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

    def validate(self, data):
        if not data or not data['operationType'] or not data['amount']:
            raise serializers.ValidationError(
                'В запросе необходимы поля "operationType" и "amount"'
            )
        if (data['operationType'] != CHANGE_CHOICES[0][0] and
            data['operationType'] != CHANGE_CHOICES[1][0]):
            raise serializers.ValidationError(
                ('Поле "operationType" принимает '
                 'значения "DEPOSIT" и "WITHDRAW"')
            )
        return data
