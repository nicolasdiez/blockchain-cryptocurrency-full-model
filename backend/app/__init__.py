import os
import random
import requests

from flask import Flask, jsonify

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

# create Flask web server
app = Flask(__name__)

# create the blockchain instance for the Node
blockchain = Blockchain()

# create Publish/Subscribe instance (PubSub) to share events and messages among the peers of the blockchain network
pubsub = PubSub(blockchain)


# 1st endpoint --> default (TODO: add a nice blockchain pic into an HTML file and render it here)
@app.route("/")
def route_default():
    return 'Welcome to the Blockchain!'


# 2nd endpoint --> return the complete blockchain data
@app.route('/blockchain')
def route_blockchain():
    # return the blockchain as a list of blocks
    return jsonify(blockchain.to_list())


# 3rd endpoint --> mine a new block
@app.route('/blockchain/mine')
def route_blockchain_mine():
    # create a new block and add it to the chain
    blockchain.add_block('endpoint test data')

    # broadcast the new added block
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)

    # response with the new created and added block
    return jsonify(block.to_dictionary())


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