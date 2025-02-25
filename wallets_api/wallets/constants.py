from decimal import Decimal

BALANCE_LENGTH = 10
DECIMAL_LENGTH = 2
DECIMAL_DEFAULT = '0.00'
CHANGE_CHOICES = (
    ('DEPOSIT', 'Deposit'),
    ('WITHDRAW', 'Withdraw')
)
MIN_CHANGE = Decimal('0.01')