import os
import random

from flask import Flask, jsonify

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

# Create Flask web server
app = Flask(__name__)

# create a blockchain instance
blockchain = Blockchain()

# create a PubSub instance
pubsub = PubSub()


# 1st endpoint -> default
@app.route("/")
def route_default():
    return 'Welcome to the Blockchain!'


# 2nd endpoint --> return the blockchain data
@app.route('/blockchain')
def route_blockchain():
    # return the blockchain as a list of blocks
    return jsonify(blockchain.to_list())


# 3rd endpoint --> mine a new block
@app.route('/blockchain/mine')
def route_blockchain_mine():
    blockchain.add_block('endpoint test data')
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    return jsonify(block.to_dictionary())


# default PORT for the application to run
PORT = 5000

# check is the environment variable PEER is present (i.e. is the app is being called by a peer instance from the CLI)
if os.environ.get('PEER') == 'True':
    # choose a random port for each PEER between a 1000 different ports
    PORT = random.randint(5001, 6000)


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