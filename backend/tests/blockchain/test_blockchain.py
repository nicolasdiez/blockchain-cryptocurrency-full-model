import pytest

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA

from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction

# number of blocks to be added to the chain used in the tests
NUMBER_OF_BLOCKS = 5


@pytest.fixture
def number_of_blocks():
    return NUMBER_OF_BLOCKS


@pytest.fixture
def blockchain_with_some_blocks(number_of_blocks):
    # create the chain with the genesis block
    blockchain = Blockchain()

    # add some blocks to the chain
    for i in range(1, number_of_blocks):
        blockchain.add_block([Transaction(Wallet(), 'recipient_address', i).to_dictionary()])
        # print(f'data-for-block-{i}: ')

    return blockchain


def test_replace_chain(blockchain_with_some_blocks):
    # create a local chain with just the genesis block
    blockchain = Blockchain()

    # replace the local blockchain with a longer chain
    blockchain.replace_chain(blockchain_with_some_blocks.chain)

    assert blockchain.chain == blockchain_with_some_blocks.chain


def test_replace_chain_not_longer(blockchain_with_some_blocks):
    # create a local chain with just the genesis block
    blockchain = Blockchain()

    # in this test we look for an Exception to be raised in the replace_chain() method
    with pytest.raises(Exception, match='Can not replace the local chain. The incoming chain must be longer'):
        blockchain_with_some_blocks.replace_chain(blockchain.chain)


def test_replace_chain_invalid_chain(blockchain_with_some_blocks):
    # create a local chain with just the genesis block
    blockchain = Blockchain()

    # tamper the hash of a block of the incoming broadcasted chain
    blockchain_with_some_blocks.chain[3].hash = 'tampered_hash'

    # in this test we look for an Exception to be raised in the replace_chain() method
    with pytest.raises(Exception, match='Can not replace the local chain. The incoming chain must be valid'):
        blockchain.replace_chain(blockchain_with_some_blocks.chain)


def test_is_valid_chain(blockchain_with_some_blocks):
    Blockchain.is_valid_chain(blockchain_with_some_blocks.chain)


def test_is_valid_chain_error_in_genesis_block(blockchain_with_some_blocks):
    blockchain_with_some_blocks.chain[0].hash = 'tampered_hash'

    # pytest.raises() tells python that next chunk of code will raise an exception
    with pytest.raises(Exception, match='The genesis block is not correct'):
        # this will raise an exception since the hash value of the genesis block has been tampered
        Blockchain.is_valid_chain(blockchain_with_some_blocks.chain)

# Validate a chain of blocks from the point of view of the transactions included on it
def test_is_valid_chain_transactions(blockchain_with_some_blocks):
    Blockchain.is_valid_chain_transactions(blockchain_with_some_blocks.chain)


def test_is_valid_chain_transactions_duplicated_transaction(blockchain_with_some_blocks):
    transaction = Transaction(Wallet(), 'recipient_dummy', 999).to_dictionary()

    blockchain_with_some_blocks.add_block([transaction, transaction])

    with pytest.raises(Exception, match="is not unique in the chain"):
        Blockchain.is_valid_chain_transactions(blockchain_with_some_blocks.chain)


def test_is_valid_chain_transactions_multiple_miner_rewards_in_block(blockchain_with_some_blocks):
    transaction_reward_1 = Transaction.generate_mining_reward_transaction(Wallet()).to_dictionary()
    transaction_reward_2 = Transaction.generate_mining_reward_transaction(Wallet()).to_dictionary()

    blockchain_with_some_blocks.add_block([transaction_reward_1, transaction_reward_2])

    with pytest.raises(Exception, match="has more than one mining reward"):
        Blockchain.is_valid_chain_transactions(blockchain_with_some_blocks.chain)


def test_is_valid_chain_transactions_with_erroneous_transaction(blockchain_with_some_blocks):
    erroneous_transaction = Transaction(Wallet(), 'recipient_dummy', 999)
    
    # change the legit signature for a new generated one
    erroneous_transaction.input['signature'] = Wallet().sign(erroneous_transaction.output)

    blockchain_with_some_blocks.add_block([erroneous_transaction.to_dictionary()])

    with pytest.raises(Exception):
        Blockchain.is_valid_chain_transactions(blockchain_with_some_blocks.chain)

def test_is_valid_chain_transactions_with_bad_historic_balance(blockchain_with_some_blocks):
    wallet = Wallet()
    bad_transaction = Transaction(wallet, 'recipient_dummy', 999)
    bad_transaction.output[wallet.address] = 1000
    bad_transaction.input['amount'] = 1999
    bad_transaction.input['signature'] = wallet.sign(bad_transaction.output)

    blockchain_with_some_blocks.add_block([bad_transaction.to_dictionary()])
    
    with pytest.raises(Exception, match="invalid input amount"):
        Blockchain.is_valid_chain_transactions(blockchain_with_some_blocks.chain)


def test_blockchain_instance():
    blockchain = Blockchain()

    # check if 1st block is actually the genesis block
    assert blockchain.chain[0].hash == GENESIS_DATA['hash']


def test_add_block():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.add_block(data)

    # check if the new block was properly added at the end of the chain
    assert blockchain.chain[-1].data == data

