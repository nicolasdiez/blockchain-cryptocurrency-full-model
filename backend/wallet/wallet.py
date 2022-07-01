import uuid
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec


class Wallet:
    """
    Represents a wallet for a miner.
    Wallet is used for:
    - Tracking the balance of the miner
    - Authorize transactions by the miner by using the pair of public/private keys
    """
    def __init__(self):
        # getting just first 6 chars to ease debugging
        self.address = str(uuid.uuid4())[:6]

        # using Standard Efficient Cryptography Prime 256-bit algorithm (bitcoin uses this one as well)
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())

        # public key is generated from private key
        self.public_key = self.private_key.public_key()

        self.balance = STARTING_BALANCE


def main():
    wallet = Wallet()
    print(f'wallet.__dict__: {wallet.__dict__}')


if __name__ == '__main__':
    main()