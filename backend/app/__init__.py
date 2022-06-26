from flask import Flask, jsonify

from backend.blockchain.blockchain import Blockchain

# Create Flask web server
app = Flask(__name__)

# create a blockchain instance
blockchain = Blockchain()

# add some dummy blocks to the chain
# for i in range(1, 3):
#     blockchain.add_block(i)


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
    return jsonify(blockchain.chain[-1].to_dictionary())


# run the Flask web server
app.run()
