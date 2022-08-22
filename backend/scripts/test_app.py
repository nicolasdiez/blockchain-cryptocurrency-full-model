import requests
from backend.wallet.wallet import Wallet
import time

BASE_URL = 'http://localhost:5000'


def get_blockchain():
    return requests.get(f'{BASE_URL}/blockchain').json()


def get_blockchain_mine():
    return requests.get(f'{BASE_URL}/blockchain/mine').json()


def post_wallet_transaction(recipient, amount):
    return requests.post(
        f'{BASE_URL}/wallet/transaction',
        json={'recipient': recipient, 'amount': amount}
    ).json()


start_blockchain = get_blockchain()
print(f'start_blockchain: {start_blockchain}')

recipient = Wallet().address

post_wallet_transaction_1 = post_wallet_transaction(recipient, 21)
print(f'\npost_wallet_transaction_1:{post_wallet_transaction_1}')

post_wallet_transaction_2 = post_wallet_transaction(recipient, 13)
print(f'\npost_wallet_transaction_2:{post_wallet_transaction_2}')

time.sleep(1)
mined_block = get_blockchain_mine()
print(f'\nmined_block:{mined_block}')
