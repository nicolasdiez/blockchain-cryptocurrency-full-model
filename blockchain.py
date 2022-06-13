from block import Block


class Blockchain:
    """
    Blockchain: is a public ledger of transactions, implemented as a linked list of Blocks.
    """

    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        last_block = self.chain[-1]
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