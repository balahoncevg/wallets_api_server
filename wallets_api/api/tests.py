from rest_framework import status
from rest_framework.test import APITestCase

from wallets.models import Wallet


class WalletAPITestCase(APITestCase):
    def setUp(self):
        """Создаём кошелёк для тестов."""
        self.wallet = Wallet.objects.create(
            balance=10000
        )
        wallet_id = self.wallet.id
        self.wallet_info_url = f'/api/v1/wallets/{wallet_id}'
        self.operation_url =  f'/api/v1/wallets/{wallet_id}/operation'
    
    def test_get_balance(self):
        """Тест на получение информации о балансе"""
        response = self.client.get(
            self.wallet_info_url, format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            'Код ответа при получении баланса кошелька должен быть 200!'
        )
        self.assertEqual(
            response.data['balance'], '10000.00',
            'Значение "balance" должно быть соответствовать заданому!'
        )
    
    def test_deposit_operation(self):
        response = self.client.post(
            self.operation_url,
            data={'operationType': 'DEPOSIT', 'amount': 1000},
            format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            'Код ответа при изменении баланса кошелька должен быть 200!'
        )
        self.assertEqual(
            response.data['balance'], '11000.00',
            'Значение "balance" должно корректно расти при пополнении!'
        )
    
    def test_withdraw_operation(self):
        response = self.client.post(
            self.operation_url,
            data={'operationType': 'WITHDRAW', 'amount': 500},
            format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            'Код ответа при изменении баланса кошелька должен быть 200!'
        )
        self.assertEqual(
            response.data['balance'], '9500.00',
            'Значение "balance" должно корректно уменьшаться при списании!'
        )
    
    def test_below_limit_withdraw_operation(self):
        response = self.client.post(
            self.operation_url,
            data={'operationType': 'WITHDRAW', 'amount': 11000},
            format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN,
            'Код ответа при привышении лимита снятия должен быть 403!'
        )
