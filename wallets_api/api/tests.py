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
        self.wrong_id_url = f'/api/v1/wallets/{reversed(str(wallet_id))}'
    
    def test_get_balance(self):
        """Тест на получение информации о балансе."""
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
    
    def test_get_wrong_wallet(self):
        """Тест получения баланса несуществующего кошелька."""
        response = self.client.get(
            self.wrong_id_url,
            format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND,
            'При обращении к несуществующему кошельку долже быть ответ 404!'
        )
    
    def test_deposit_operation(self):
        """Тест на пополнение кошелька."""
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
        """Тест на списание с кошелька."""
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
        """Тест на списание сверх имеющихся средств."""
        response = self.client.post(
            self.operation_url,
            data={'operationType': 'WITHDRAW', 'amount': 11000},
            format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN,
            'Код ответа при привышении лимита снятия должен быть 403!'
        )
    
    def test_invalid_operation_type(self):
        """Тест на тип операции."""
        response = self.client.post(
            self.operation_url,
            data={'operationType': 'ADD', 'amount': 1000},
            format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            ('Поле "operationType" должно принимать только '
             'значения "DEPOSIT" и "WITHDRAW"!')
        )
    
    def test_negative_amount_operation(self):
        """Тест на попытку операции с отрицательным числом."""
        response = self.client.post(
            self.operation_url,
            data={'operationType': 'DEPOSIT', 'amount': -1000},
            format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            'Значение поля "" должно быть положительным числом!'
        )
    
    def test_operation_amount_type(self):
        """Тест на тип данных для поля 'operationType'."""
        response = self.client.post(
            self.operation_url,
            data={'operationType': 'WITHDRAW', 'amount': 'word'},
            format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            'Значение поля "amount" должно быть положительным числом!'
        )
    
    def test_no_operation_type(self):
        """Тест на отсутствие поля 'operationType'."""
        response = self.client.post(
            self.operation_url,
            data={'amount': 'word'},
            format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            'Поле "operationType" должно быть обязательным!'
        )
    
    def test_no_operation_type(self):
        """Тест на отсутствие поля 'amount'."""
        response = self.client.post(
            self.operation_url,
            data={'operationType': 'WITHDRAW'},
            format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            'Поле "amount" должно быть обязательным!'
        )
    
    def test_empty_operation(self):
        """Тест на пустой запрос для изменения баланса."""
        response = self.client.post(
            self.operation_url,
             data={},
            format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST,
            'Поля "operationType" и "amount" должны быть обязательными!'
        )

    def test_wrong_wallet_operation(self):
        """Тест изменения баланса несуществующего кошелька."""
        response = self.client.get(
            str.join(self.wrong_id_url, '/operation'),
            data={'operationType': 'DEPOSIT', 'amount': 1000},
            format='json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND,
            'При пополнении несуществующего кошелька долже быть ответ 404!'
        )
