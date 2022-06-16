from backend.blockchain.block import Block


class Blockchain:
    """
    Blockchain: is a public ledger of transactions, implemented as a linked list of Blocks.
    """

    def __init__(self):
        # first block of the chain is always the genesis block
        self.chain = [Block.genesis()]

    def add_block(self, data):
        # new block to be added always depends on the last current block of the chain (BLOCK-CHAIN)
        last_block = self.chain[-1]

        # the new block is added at the end of the chain
        self.chain.append(Block.mine_block(last_block, data))

    def __repr__(self):  # method to see the Blockchain objects as strings
        return f'Blockchain: {self.chain}'


def main():  # including debug code here, so it only executes when directly call this file from cli
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)
    print(f'blockchain.py __name__: {__name__}')


if __name__ == '__main__':
    main()