import pytest

from backend.wallet.wallet import Wallet

from backend.blockchain.blockchain import Blockchain
from backend.config import STARTING_BALANCE

from backend.wallet.transaction import Transaction

@pytest.fixture
def data_test():
    return {'test_key': 'test_data'}


def test_verify_valid_signature(data_test):
    wallet = Wallet()
    signature = wallet.sign(data_test)

    # verify_signature() returns True if verification is OK
    assert Wallet.verify_signature(wallet.public_key, data_test, signature)


def test_verify_invalid_signature(data_test):
    wallet = Wallet()
    signature = wallet.sign(data_test)

    # verify_signature() returns False if verification is NOT OK
    # generate a new random wallet with its public_key to verify the signature
    assert not Wallet.verify_signature(Wallet().public_key, data_test, signature)


def test_calculate_balance_no_transactions():
    wallet = Wallet()
    blockchain = Blockchain()

    # if no transactions are made by the Wallet (address) its balance should be the starting balance
    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE


def test_calculate_balance_wallet_sends_transaction():
    wallet = Wallet()
    blockchain = Blockchain()

    amount_to_send = 10
    transaction_send = Transaction(wallet, 'recipient-address', amount_to_send)

    blockchain.add_block([transaction_send.to_dictionary()])

    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE - amount_to_send


def test_calculate_balance_wallet_receives_transaction():
    sender_wallet = Wallet()
    recipient_wallet = Wallet()
    blockchain = Blockchain()

    amount_received_1 = 15
    transaction_received_1 = Transaction(sender_wallet, recipient_wallet.address, amount_received_1)

    amount_received_2 = 3
    transaction_received_2 = Transaction(sender_wallet, recipient_wallet.address, amount_received_2)

    blockchain.add_block([transaction_received_1.to_dictionary(), transaction_received_2.to_dictionary()])

    assert Wallet.calculate_balance(blockchain, recipient_wallet.address) == STARTING_BALANCE + amount_received_1 + \
        amount_received_2


def calculate_balance_wallet_sends_and_receives_transactions():
    sender_receiver_wallet = Wallet()
    wallet = Wallet()
    blockchain = Blockchain()

    amount_to_send = 10
    transaction_send = Transaction(sender_receiver_wallet, wallet.address, amount_to_send)

    amount_received_1 = 15
    transaction_received_1 = Transaction(wallet, sender_receiver_wallet.address, amount_received_1)

    amount_received_2 = 3
    transaction_received_2 = Transaction(wallet, sender_receiver_wallet.address, amount_received_2)

    blockchain.add_block([transaction_send.to_dictionary(), transaction_received_1.to_dictionary(),
                          transaction_received_2.to_dictionary()])

    assert Wallet.calculate_balance(blockchain, sender_receiver_wallet.address) == \
           STARTING_BALANCE - amount_to_send + amount_received_1 + amount_received_2
