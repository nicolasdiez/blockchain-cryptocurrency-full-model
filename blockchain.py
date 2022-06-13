class Block:
    """
    Block: unit of storage in a blockchain network that supports cryptocurrency.
    A Block contains 1 or more transactions.
    A transaction is a transfer of cryptocurrency between 2 participants
    lalalalala
    """
    def __init__(self, data):
        self.data = data

    def __repr__(self):   # __repr__ is a special method used to represent a class's objects as a string
        return f'Block - data: {self.data}'  # __repr__ is called by the repr() built-in function


class Blockchain:
    """
    Blockchain: is a public ledger of transactions, implemented as a linked list of Blocks.
    """

    def __init__(self):
        self.chain = []

    def add_block(self, data):
        self.chain.append(Block(data))

    def __repr__(self):  # method to see the Blockchain objects as strings
        return f'Blockchain: {self.chain}'


blockchain = Blockchain()
blockchain.add_block('one')
blockchain.add_block('two')

print(blockchain)