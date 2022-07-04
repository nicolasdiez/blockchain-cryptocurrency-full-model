from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
import pytest


def test_transaction():
    sender_wallet = Wallet()
    recipient_address = 'recipient'
    amount = 15
    transaction = Transaction(sender_wallet, recipient_address, amount)

    assert transaction.output[recipient_address] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount

    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == sender_wallet.balance
    assert transaction.input['address'] == sender_wallet.address
    assert transaction.input['public_key'] == sender_wallet.public_key

    assert Wallet.verify_signature(transaction.input['public_key'], transaction.output, transaction.input['signature'])


def test_transaction_balance_exceeded():
    # expecting an exception to be raised when creating the Transaction (20000 > STARTING_BALANCE)
    with pytest.raises(Exception, match="Amount exceeds sender's balance"):
        Transaction(Wallet(), 'recipient', 20000)