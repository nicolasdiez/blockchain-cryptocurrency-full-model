import uuid
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature


class Wallet:
    """
    Represents a wallet for a peer on the blockchain network (i.e. a miner).
    Wallet is used for:
    - Tracking the balance of the peer (miner)
    - Authorize transactions by the peer (miner) by using the pair of public/private keys
    """
    def __init__(self, blockchain=None):
        # just getting the first 8 chars of the random uuid generated as the wallet address to ease debugging
        self.address = str(uuid.uuid4())[:8]

        # using Standard Efficient Cryptography Prime 256-bit algorithm (bitcoin uses this one as well)
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())

        # public key is generated from private key
        self.public_key = self.private_key.public_key()

        # Transform the format of the public key into a series of bytes
        self.serialize_public_key()

        self.blockchain = blockchain

    # re-calculate balance of the Wallet everytime the balance is accessed
    @property
    def balance(self):
        return Wallet.calculate_balance(self.blockchain, self.address)

    def sign(self, data):
        """
        Create a signature from the input data and the local private key
        Signature = Data + Private_Key
        Only the owner of the local private key can generate signatures from the input data
        """
        return decode_dss_signature(self.private_key.sign(
            json.dumps(data).encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
            )
        )

    @staticmethod
    def verify_signature(public_key, data, signature):
        """
        Verify a signature based on the input data and the public key associated to the private key used to sign
        """
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )

        # print(f'\nsignature:{signature}')

        # get the separated tuple values
        (r, s) = signature

        try:
            deserialized_public_key.verify(encode_dss_signature(r,s),
                                           json.dumps(data).encode('utf-8'),
                                           ec.ECDSA(hashes.SHA256()))
            return True
        # instead of a genetic Exception, catch the specific InvalidSignature exception from public_key.verify() method
        except InvalidSignature:
            return False

    def serialize_public_key(self):
        """
        Transform the public key into a series of bytes
        """
        public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        decoded_public_key = public_key_bytes.decode('utf-8')

        self.public_key = decoded_public_key

        # print(f'self.public_key: {self.public_key}')

    @staticmethod
    def calculate_balance(blockchain, address):
        """
        Determine the balance of the given address by checking the transaction data within the blockchain.

        The balance for a specific address is found by adding the output values that belong to the address
        since the most recent transaction by that address.

        Note that when a wallet makes a transaction it officially resets its balance.
        """
        balance = STARTING_BALANCE

        # prevent crash in case Wallet is instanced without providing a blockchain as input
        if not blockchain:
            return balance

        for block in blockchain.chain:
            for transaction in block.data:
                # check if the address has initiated a transaction
                if transaction['input']['address'] == address:
                    # every time an address initiates a new transaction it resets its balance (taken from the output)
                    balance = transaction['output'][address]
                # check if the address is a recipient of a transaction
                elif address in transaction['output']:
                    balance += transaction['output'][address]

        return balance


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