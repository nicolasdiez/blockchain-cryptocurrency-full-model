from backend.blockchain.block import Block, GENESIS_DATA
import time
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary


def test_mined_block_quickly():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    mined_block = Block.mine_block(last_block, 'bar')

    # assuming current mined_block is going to be mined quickly since it´s next line of code from mining the last_block
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
    time.sleep(MINE_RATE / SECONDS)  # simulate that the current mined_block is mined slowly
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

