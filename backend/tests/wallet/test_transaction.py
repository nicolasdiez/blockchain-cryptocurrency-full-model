from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
import pytest


def test_transaction():
    sender_wallet = Wallet()
    recipient_address = 'recipient-test-address'
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
        sender_wallet = Wallet()
        recipient_address = 'recipient-test-address'
        amount = 20000
        Transaction(sender_wallet, recipient_address, amount)


def test_update_transaction_balance_exceeded():
    sender_wallet = Wallet()
    recipient_address = 'recipient-test-address'
    amount = 15
    transaction = Transaction(sender_wallet, recipient_address, amount)

    # expecting an exception to be raised when creating the Transaction (20000 > STARTING_BALANCE)
    with pytest.raises(Exception, match="Amount exceeds sender's balance"):
        updated_recipient_address = 'updated-recipient-test-address'
        updated_amount = 20000
        transaction.update_transaction(sender_wallet, updated_recipient_address, updated_amount)


def test_update_transaction_successfully_new_recipient():
    # generate a 1st transaction to one recipient
    sender_wallet = Wallet()
    recipient_address = 'recipient-test-address'
    amount = 15
    transaction = Transaction(sender_wallet, recipient_address, amount)

    # update the current transaction to include a 2nd recipient
    next_recipient_address = 'next-recipient-test-address'
    next_amount = 25
    transaction.update_transaction(sender_wallet, next_recipient_address, next_amount)

    assert transaction.output[next_recipient_address] == next_amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount - next_amount

    # True is excepted to be returned by verify_signature()
    assert Wallet.verify_signature(transaction.input['public_key'], transaction.output, transaction.input['signature'])


def test_update_transaction_successfully_same_recipient():
    # generate a 1st transaction to one recipient
    sender_wallet = Wallet()
    recipient_address = 'recipient-test-address'
    amount = 15
    transaction = Transaction(sender_wallet, recipient_address, amount)

    # add amount to the same 1st recipient
    new_amount = 75
    transaction.update_transaction(sender_wallet, recipient_address, new_amount)

    assert transaction.output[recipient_address] == amount + new_amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount - new_amount

    # True is excepted to be returned by verify_signature()
    assert Wallet.verify_signature(transaction.input['public_key'], transaction.output, transaction.input['signature'])


def test_validate_transaction_transaction_ok():
    sender_wallet = Wallet()
    recipient_address = 'recipient-test-address'
    amount = 15
    Transaction.is_valid_transaction(Transaction(sender_wallet, recipient_address, amount))


def test_validate_transaction_invalid_output():
    sender_wallet = Wallet()
    recipient_address = 'recipient-test-address'
    amount = 15
    transaction = Transaction(sender_wallet, recipient_address, amount)

    # tamper the output balance for the sender wallet
    transaction.output[sender_wallet.address] = 5000

    # expected an exception to be raised here due to the tampering of the output sender's wallet balance
    with pytest.raises(Exception, match='Error in the output transaction balance'):
        Transaction.is_valid_transaction(transaction)


def test_validate_transaction_invalid_signature():
    sender_wallet = Wallet()
    recipient_address = 'recipient-test-address'
    amount = 15
    transaction = Transaction(sender_wallet, recipient_address, amount)

    # sign the same output data but with a different private key from a new Wallet
    new_signature = Wallet().sign(transaction.output)

    transaction.input['signature'] = new_signature

    # expected an exception to be raised here due to the tampering of the signature
    # reminder --> signature = data + private_key
    with pytest.raises(Exception, match='Error in transaction signature'):
        Transaction.is_valid_transaction(transaction)