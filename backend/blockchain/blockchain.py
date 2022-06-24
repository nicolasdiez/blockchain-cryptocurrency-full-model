from backend.blockchain.block import Block


class Blockchain:
    """
    Blockchain: is a public ledger of transactions, implemented as a linked list of Blocks.
    """

    def __init__(self):
        # first block of the chain is always the genesis block
        self.chain = [Block.genesis()]

    def __repr__(self):  # method to print the Blockchain objects as strings
        return f'Blockchain: {self.chain}'

    def add_block(self, data):
        # the new block to be added always depends on the last current block of the chain (BLOCK-CHAIN)
        last_block = self.chain[-1]

        # the new block is added at the end of the chain
        self.chain.append(Block.mine_block(last_block, data))

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate a chain of blocks by ensuring the following criteria are met:
        1- a chain must always start with the genesis block
        2- blocks forming the chain must have the correct format
        """

        # validate every block, except for the 1st one (i.e. the genesis block)
        for i in range(1, len(chain)):
            current_block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, current_block)

        if chain[0] != Block.genesis():
            raise Exception ('The genesis block is not correct')


def main():  # including debug code here, so it only executes when directly call this file from cli
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)
    print(f'blockchain.py __name__: {__name__}')


if __name__ == '__main__':
    main()