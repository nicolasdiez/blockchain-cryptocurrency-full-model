import time
import sys
from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE, SECONDS

# declared as global dictionary variable to be passed as **kwargs argument
GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,  # initial difficulty
    'nonce': 'genesis_nonce'
}


class Block:
    """
    Block: unit of storage in a blockchain network.
    A Block contains 1 or more transactions of cryptocurrency.
    """

    # Constructor
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    # reminder: __repr__ is a special method used to represent a class's objects as a string
    def __repr__(self):
        # __repr__ is called by the repr() built-in function (therefore, it´s called by the print() built-in function)
        return (
            'Block('f'\n'
            f'timestamp: {self.timestamp},\n'
            f'last_hash: {self.last_hash},\n'
            f'hash: {self.hash},\n'    
            f'data: {self.data},\n'
            f'difficulty: {self.difficulty},\n'
            f'nonce: {self.nonce})\n'
        )

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and current data.
        To mine means finding a 'nonce' number that produces a 'hashed' block value with 'difficulty' leading zeros.
        This approach is the so-called Proof of Work consensus.
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)  # difficulty adjusted dynamically w/ each new block
        nonce = 0  # first nonce value to try
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        # Proof of Work
        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()  # regenerate timestamp to be as accurate as possible (find nonce may take time)
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    # Another implementation option for the mine_block method
    def mine_block_2(self, last_block):
        self.timestamp = time.time_ns()
        last_hash = last_block.hash
        self.difficulty = Block.adjust_difficulty(last_block, self.timestamp)
        self.hash = crypto_hash(self.timestamp, last_hash, self.data, self.difficulty, self.nonce)

        # Proof of Work
        while hex_to_binary(self.hash)[0:self.difficulty] != '0' * self.difficulty:
            self.nonce += 1
            self.timestamp = time.time_ns()  # regenerate timestamp to be as accurate as possible (loop may take time)
            self.difficulty = Block.adjust_difficulty(last_block, self.timestamp)
            self.hash = crypto_hash(self.timestamp, last_hash, self.data, self.difficulty, self.nonce)

        return sys.exit()

    @staticmethod
    def genesis():
        """
        Generate the genesis block of the blockchain
        """
        # return Block(
        #     timestamp=GENESIS_DATA['timestamp'],
        #     last_hash=GENESIS_DATA['last_hash'],
        #     hash=GENESIS_DATA['hash'],
        #     data=GENESIS_DATA['data']
        # )

        # using **kwargs to allow more/fewer arguments added/removed from the genesis block
        return Block(**GENESIS_DATA)

    @staticmethod
    def adjust_difficulty(last_block, timestamp):
        """
        Increases or decreases the difficulty of the next block based on how long it's taking to mine the new block.
        Increase difficulty if the current block is being mined quickly (current mining time < MINE_RATE).
        Decrease difficulty if the current block is being mined slowly (current mining time > MINE_RATE).
        """

        # block is being mined quickly (time elapsed from last mined block has not yet reached MINE_RATE seconds)
        if (timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        # block is being mined slowly (time elapsed from last mined block has already passed MINE_RATE seconds)
        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        # in any other case, return the minimum limited difficulty value of 1
        return 1

    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validate a block by ensuring the following criteria are met:
        1- block must have the correct last_hash reference to the previous last_block
        2- block must meet the PoW requirement ('difficulty' number of leading zeros)
        3- block´s difficulty must only be adjusted by 1 with respect to the last_block
        4- actual hashing of the block must meet the hash value field written in the block itself
        """

        if block.last_hash != last_block.hash:
            raise Exception('last_hash in current block does not match hash value in the last block')

        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('Proof of Work leading zeros requirement not achieved')

        # only allowing a maximum difficulty adjustment between neighbour blocks of 1
        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception("Block difficulty can not be adjusted by more than 1 respect of the last block's")

        # block.hash value not included because the hash in fact the value that crypto_hash calculates
        re_calculated_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce)

        if re_calculated_hash != block.hash:
            return Exception('The block hash is not correct')


# main() used to debug, it only executes when directly calling this file from cli
def main():
    print('Executing -- block.py main()')
    # genesis_block = Block.genesis()
    # block = Block.mine_block(genesis_block, 'foo')
    # block = genesis_block.mine_block_2()
    # print(block)

    genesis_block = Block.genesis()
    bad_block = Block.mine_block(genesis_block, 'foo')
    bad_block.last_hash = 'evil_data'

    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e:
        print(f'is_valid_block: {e}')

if __name__ == '__main__':
    main()
