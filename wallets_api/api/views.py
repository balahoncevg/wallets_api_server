from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from wallets.models import Wallet
from .serializers import ChangeBalanceSerializer, WalletSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    http_method_names = ['get', 'post', 'delete']
    serializer_class = WalletSerializer

    @action(
        detail=True, methods = ['post',],
        url_path='operation',
        url_name='operation',
    )
    def operation(self, request, pk=None):
        get_object_or_404(Wallet, pk=pk)
        serializer = ChangeBalanceSerializer(
            data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(pk=pk)
                amount = data['amount']
                if data['operationType'] == 'DEPOSIT':
                    wallet.balance += amount
                elif data['operationType'] == 'WITHDRAW':
                    if wallet.balance < amount:
                        return Response(
                            status=status.HTTP_403_FORBIDDEN
                        )
                    wallet.balance -= amount
                wallet.save()
                return Response(
                    WalletSerializer(wallet).data
                )
