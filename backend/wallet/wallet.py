import uuid
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import json


class Wallet:
    """
    Represents a wallet for a peer on the blockchain network (i.e. a miner).
    Wallet is used for:
    - Tracking the balance of the peer (miner)
    - Authorize transactions by the peer (miner) by using the pair of public/private keys
    """
    def __init__(self):
        # getting just first 6 chars to ease debugging
        self.address = str(uuid.uuid4())[:6]

        # using Standard Efficient Cryptography Prime 256-bit algorithm (bitcoin uses this one as well)
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())

        # public key is generated from private key
        self.public_key = self.private_key.public_key()

        self.balance = STARTING_BALANCE

    def sign(self, data):
        """
        Create a signature from the input data and the local private key
        Signature = Data + Private_Key
        Only the owner of the local private key can generate signatures from the input data
        """
        return self.private_key.sign(json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))

    @staticmethod
    def verify_signature(public_key, data, signature):
        """
        Verify a signature based on the input data and the public key associated to the private key used to sign
        """
        try:
            public_key.verify(signature, json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))
            return True
        # instead of a genetic Exception, catch the specific InvalidSignature exception from public_key.verify() method
        except InvalidSignature:
            return False


def main():
    wallet = Wallet()
    print(f'wallet.__dict__: {wallet.__dict__}')

    data = {'foo': 'bar'}
    signature = wallet.sign(data)
    print(f'signature:{signature}')

    should_be_valid = Wallet.verify_signature(wallet.public_key, data, signature)
    print(f'should_be_valid:{should_be_valid}')

    should_be_invalid = Wallet.verify_signature(Wallet().public_key, data, signature)
    print(f'should_be_invalid:{should_be_invalid}')


if __name__ == '__main__':
    main()