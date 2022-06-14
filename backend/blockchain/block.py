import time
from backend.util.crypto_hash import crypto_hash


class Block:
    """
    Block: unit of storage in a blockchain network that supports cryptocurrency.
    A Block contains 1 or more transactions.
    """
    def __init__(self, timestamp, last_hash, hash, data):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data

    def __repr__(self):   # __repr__ is a special method used to represent a class's objects as a string
        # __repr__ is called by the repr() built-in function
        return (
            'Block(' 
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '    
            f'data: {self.data}) '
        )

    def mine_block_2(self):
        timestamp = time.time_ns()
        last_hash = self.hash
        hash = f'{timestamp}-{last_hash}'

        return Block(timestamp, last_hash, hash, self.data)

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        hash = crypto_hash(timestamp, last_hash, data)

        return Block(timestamp, last_hash, hash, data)

    @staticmethod
    def genesis():
        """
        Generate the genesis block of the blockchain
        """
        return Block(1, 'genesis_last_hash', 'genesis_hash', [])


def main():  # created to include debug code here, so it only executes when directly calling this file from cli
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'foo')
    # block = genesis_block.mine_block_2()
    print(block)


if __name__ == '__main__':
    main()

