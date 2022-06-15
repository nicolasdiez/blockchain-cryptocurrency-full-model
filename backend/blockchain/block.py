import time
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
    Block: unit of storage in a blockchain network that supports cryptocurrency.
    A Block contains 1 or more transactions.
    """
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):   # __repr__ is a special method used to represent a class's objects as a string
        # __repr__ is called by the repr() built-in function (then, it´s called by the print() built-in function)
        return (
            'Block('f'\n'
            f'timestamp: {self.timestamp},\n'
            f'last_hash: {self.last_hash},\n'
            f'hash: {self.hash},\n'    
            f'data: {self.data},\n'
            f'difficulty: {self.difficulty},\n'
            f'nonce: {self.nonce})\n'
        )

    def mine_block_2(self):
        timestamp = time.time_ns()
        last_hash = self.hash
        hash = f'{timestamp}-{last_hash}'

        return Block(timestamp, last_hash, hash, self.data)

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data.
        To mine means finding a 'nonce' number that produces a 'hash' block value with 'difficulty' leading zeros.
        This approach is the so-called Proof of Work consensus.
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        # Proof of Work
        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()  # regenerate timestamp to be as accurate as possible (find nonce may take time)
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

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
        return Block(**GENESIS_DATA)

    @staticmethod
    def adjust_difficulty(last_block, timestamp):
        """
        Calculate the new difficulty value according to the MINE_RATE.
        Increase difficulty if the current block is being mined quickly (current mining time < MINE_RATE).
        Decrease difficulty if the current block is being mined slowly (current mining time > MINE_RATE).
        """

        if (timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        # in any other case, return the minimum limited difficulty value of 1
        return 1


def main():  # created to include debug code here, so it only executes when directly calling this file from cli
    print('Executing -- block.py main()')
    # genesis_block = Block.genesis()
    # block = Block.mine_block(genesis_block, 'foo')
    # block = genesis_block.mine_block_2()
    # print(block)

    last_block = Block(
        time.time_ns(),
        'test_last_hash',
        'test_hash',
        'test_data',
        1,
        0
    )
    time.sleep(MINE_RATE / SECONDS)  # simulate that the current mined_block is mined slowly
    print(last_block)
    mined_block = Block.mine_block(last_block, 'bar')
    print(mined_block)


if __name__ == '__main__':
    main()

