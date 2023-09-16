import requests
from backend.wallet.wallet import Wallet
import time

LOCALHOST_BASE_URL = 'http://localhost:5000'


# consume endpoint GET /blockchain
def get_blockchain():
    # get the blockchain (= the list of blocks)
    return requests.get(f'{LOCALHOST_BASE_URL}/blockchain').json()


# consume endpoint GET /blockchain/mine
def get_blockchain_mine():
    # mine, add, and then retrieve, a new block to the chain
    return requests.get(f'{LOCALHOST_BASE_URL}/blockchain/mine').json()


# consume endpoint POST /wallet/transaction
def post_wallet_transaction(recipient, amount):
    # add a transaction to the transaction pool
    return requests.post(
        f'{LOCALHOST_BASE_URL}/wallet/transaction',
        json={'recipient': recipient, 'amount': amount}
    ).json()


start_blockchain = get_blockchain()
print(f'start_blockchain: {start_blockchain}')

# create a wallet for the recipient of the transactions we are gonna make and get its addresss
recipient = Wallet().address

# make some transactions, so they are added to the transaction pool
transaction_1 = post_wallet_transaction(recipient, 100)
print(f'\ntransaction_1:{transaction_1}')

time.sleep(0.5)

transaction_2 = post_wallet_transaction(recipient, 53)
print(f'\ntransaction_2:{transaction_2}')

time.sleep(0.5)

transaction_3 = post_wallet_transaction(recipient, 27)
print(f'\ntransaction_3:{transaction_3}')

# let some time pass so all the nodes in the network have time to receive the events with the new transactions
# and have their local chains updated before the mining of a new block starts
time.sleep(2)

block_mined = get_blockchain_mine()
print(f'\nblock_mined:{block_mined}')
