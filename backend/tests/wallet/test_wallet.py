import pytest

from backend.wallet.wallet import Wallet


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
