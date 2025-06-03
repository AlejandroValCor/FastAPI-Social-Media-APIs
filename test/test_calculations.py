# You need to make sure the name of the file is called test_*.py orpytest -v *_text.py
import pytest
from app.calculations import add, substract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(100)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (5, 8, 13),
    (1, 85, 86)
])
def test_add(num1, num2, expected):
    # Sum should be equal to 14
    assert add(num1, num2) == expected

def test_substract():
    # Substract should be equal to 7
    assert substract(12, 5) == 7

def test_multiply():
    # Multiply should be equal to 20
    assert multiply(4, 5) == 20

def test_divide():
    # Divide should be equal to 3
    assert divide(15, 5) == 3

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 100

def test_bank_default_amount(zero_bank_account):  
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(40)

    assert bank_account.balance == 60

def test_deposit(bank_account):
    bank_account.deposit(60)

    assert bank_account.balance == 160

def test_collect_interest(bank_account):
    bank_account.collect_interest()

    assert round(bank_account.balance, 6) == 110

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (150, 50, 100),
    (200, 100, 100),
    (5655, 650, 5005),
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)

    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(500)