from backend.util.crypto_hash import crypto_hash


def test_crypto_hash():
    # crypto_hash method should return the same hash value with arguments of different data types in any given order
    assert crypto_hash(2, 'one', [3]) == crypto_hash([3], 2, 'one')

    # master hash testing of a fixed data entry
    assert crypto_hash('test-cryptohash-method') == '948db9dc2aec86f31a30bd7747818d0fbd8cac7866e8b0923c9b5272c85271ed'

