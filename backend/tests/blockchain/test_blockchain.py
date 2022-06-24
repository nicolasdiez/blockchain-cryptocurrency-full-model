import pytest

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA

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
        blockchain.add_block(f'data-for-block-:{i}')
        print(f'data-for-block-{i}')

    return blockchain


def is_valid_chain_error_in_genesis_block(blockchain_with_some_blocks(5)):
    blockchain_with_some_blocks.chain[0].hash = 'tampered_hash'

    # pytest.raises() tells python that next chunk of code will raise an exception
    with pytest.raises(Exception, match='last_hash in current block does not match hash value in the last block'):
        # this will raise an exception since the hash value of the genesis block has been tampered
        Blockchain.is_valid_chain(blockchain_with_some_blocks.chain)


def test_is_valid_chain(blockchain_with_some_blocks(5)):
    Blockchain.is_valid_chain(blockchain_with_some_blocks.chain)


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

