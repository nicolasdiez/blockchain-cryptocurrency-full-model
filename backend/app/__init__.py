import os
import random
import requests

from flask import Flask, jsonify, request

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool


# create Flask web server
app = Flask(__name__)

# create the blockchain instance for the Node
blockchain = Blockchain()

# create a transaction pool instance to store all the generated transactions from the nodes
transaction_pool = TransactionPool()

# create Publish/Subscribe instance (PubSub) to share events and messages among the peers of the blockchain network
pubsub = PubSub(blockchain, transaction_pool)

# create Wallet instance
wallet = Wallet(blockchain)
print(f'\n -- My address is: {wallet.address}')


# 1st endpoint --> default (TODO: add a nice blockchain pic into an HTML file and render it here)
@app.route("/", methods=['GET'])
def route_default():
    return 'Welcome to the Blockchain!'


# 2nd endpoint --> return the complete blockchain data
@app.route('/blockchain', methods=['GET'])
def route_blockchain():
    # return the blockchain as a list of blocks
    return jsonify(blockchain.to_list())


# 3rd endpoint --> mine a new block
@app.route('/blockchain/mine', methods=['GET'])
def route_blockchain_mine():

    # get all the transactions present in the transaction pool in json serialized format
    transactions_pool_json = transaction_pool.to_json_serialized()

    # include the reward transaction for myself (as a miner) into the transaction pool
    transactions_pool_json.append(Transaction.generate_mining_reward_transaction(wallet).to_dictionary())

    # create a new block with all the transactions from the pool and add it to the chain
    blockchain.add_block(transactions_pool_json)

    # broadcast the new added block to the chain
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)

    # once the new block is broadcasted, delete the transactions which have been added to the blockchain from the
    # transactions pool
    transaction_pool.clear_transactions(blockchain)

    # response with the new created and added block
    return jsonify(block.to_dictionary())


# 4th endpoint --> generate a transaction
@app.route('/wallet/transaction', methods=['POST'])
def route_wallet_transaction():
    print('\n-- endpoint wallet/transaction')
    # format of the JSON received in the POST body request --> {'recipient': 'xxx' , 'amount': '100'}
    transaction_data = request.get_json()

    # check if there is already a transaction in the pool initiated from the 'address'
    transaction = transaction_pool.find_existing_transaction(wallet.address)

    # if there is a transaction in the pool already initiated by the 'address', then update the transaction w/ new data
    if transaction:
        transaction.update_transaction(wallet, transaction_data['recipient'], transaction_data['amount'])
    # otherwise, just create a new transaction
    else:
        transaction = Transaction(wallet, transaction_data['recipient'], transaction_data['amount'])

    # every time a new transaction is generated through this endpoint, the transaction is broadcasted to all nodes
    pubsub.broadcast_transaction(transaction)

    return jsonify(transaction.to_dictionary())


# 5th endpoint --> return wallet data (address and balance) for the provided wallet
@app.route('/wallet/data', methods=['GET'])
def route_wallet_data():
    return jsonify({'address': wallet.address, 'balance': wallet.balance})


# port only used by the 1st node of the network. This 1st node holds the complete chain from the beginning in his ledger
ROOT_PORT = 5000

PORT = ROOT_PORT

# for the rest of the nodes of the network (excepting the 1st one) a new different port is used
if os.environ.get('PEER') == 'True':
    # choose a random port for each PEER between 1000 different ports
    PORT = random.randint(5001, 6000)

    # synchronize the chain for the new peer by retrieving the complete chain from the first node of the network
    result = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    print(f'result.json():{result.json()}')

    result_blockchain = Blockchain.from_list(result.json())

    try:
        blockchain.replace_chain(result_blockchain.chain)
        print('\n-- Local chain synchronized successfully')
    except Exception as exception:
        print(f'\n-- Error synchronizing local chain: {exception}')


# run the Flask web server
app.run(port=PORT)


def main():
    pubsub.remove_listener()


if __name__ == '__main__':
    print(f'Starting: {__name__}')
    main()
    print(f'Finishing: {__name__}')
    # sys.exit()
    os._exit(0)