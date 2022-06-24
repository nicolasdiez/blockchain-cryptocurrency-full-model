import pytest

from backend.blockchain.block import Block, GENESIS_DATA
import time
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary
import pytest


# because a lot of tests are using these 2 objects (last_block and current_block), we declare them as @fixtures
@pytest.fixture
def last_block():
    return Block.genesis()


@pytest.fixture
def current_block(last_block):
    return Block.mine_block(last_block, 'data-test')


def test_is_valid_block(last_block, current_block):

    # These objects are now created in the @fixtures, so we dont need them here anymore
    # last_block = Block.genesis()
    # current_block = Block.mine_block(last_block, 'data-test')

    # if the method doesnt raise an exception the test passes implicitly
    Block.is_valid_block(last_block, current_block)


def test_is_valid_block_error_in_last_hash(last_block, current_block):

    # These objects are now created in the @fixtures, so we dont need them here anymore
    # last_block = Block.genesis()
    # current_block = Block.mine_block(last_block, 'data-test')

    # alter value of the last block hash in the current block
    current_block.last_hash = 'tampered_last_hash'

    # raises() tells Python that next chunk of code will raise an exception -> so we catch it and check if it´s expected
    # with 'match' param we compare if the exception text message thrown by is_valid_block() is the one expected
    # if the exception text thrown by Block.is_valid_block() matches the text in 'match=...', then the test is OK
    with pytest.raises(Exception, match='last_hash in current block does not match hash value in the last block'):
        # this will raise an exception since the last hash value has been tampered
        Block.is_valid_block(last_block, current_block)


def is_valid_block_error_in_proof_of_work(last_block, current_block):
    current_block.hash = '12345'

    with pytest.raises(Exception, match='Proof of Work leading zeros requirement not achieved'):
        Block.is_valid_block(last_block, current_block)


def is_valid_block_raised_difficulty(last_block, current_block):
    raised_difficulty = 10
    current_block.difficulty = raised_difficulty
    current_block.hash = f'{"0" * raised_difficulty}nico1234'

    with pytest.raises(Exception, match='Block difficulty can not be adjusted by more than 1'):
        Block.is_valid_block(last_block, current_block)


def is_valid_block_error_in_block_hash(last_block, current_block):
    current_block.hash = '000000000000nico1234567'  # with the zeros we assure the PoW is met, so we want to check hash

    with pytest.raises(Exception, match='The block hash is not correct'):
        Block.is_valid_block(last_block, current_block)


def test_mined_block_quickly():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    mined_block = Block.mine_block(last_block, 'bar')

    # assuming current mined_block is going to be mined quickly since it´s next line of code after mining the last_block
    assert mined_block.difficulty == last_block.difficulty + 1


def test_mined_block_slowly():
    last_block = Block.mine_block(Block.genesis(), 'foo')

    # wait at least MINE_RATE (in seconds) to make sure the current mined_block is mined slowly
    time.sleep(MINE_RATE / SECONDS)

    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == last_block.difficulty - 1


def test_mined_block_difficulty_limits_low_at_1():
    last_block = Block(
        time.time_ns(),
        'test_last_hash',
        'test_hash',
        'test_data',
        1,
        0
    )
    time.sleep(MINE_RATE / SECONDS)  # to simulate that the current mined_block is mined slowly
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == 1


def test_mine_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)  # check if object 'block' is actually an instance of class 'Block'
    assert block.data == data
    assert block.last_hash == last_block.hash

    assert hex_to_binary(block.hash)[0:block.difficulty] == '0' * block.difficulty


def test_genesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)  # check if object 'block' is actually an instance of class 'Block'
    # assert genesis.timestamp == GENESIS_DATA['timestamp']
    # assert genesis.last_hash == GENESIS_DATA['last_hash']
    # assert genesis.hash == GENESIS_DATA['hash']
    # assert genesis.data == GENESIS_DATA['data']
    for key, value in GENESIS_DATA.items():
        getattr(genesis, key) == value

