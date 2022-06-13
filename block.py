class Block:
    """
    Block: unit of storage in a blockchain network that supports cryptocurrency.
    A Block contains 1 or more transactions.
    lalalal
    lalalal
    """
    def __init__(self, data):
        self.data = data

    def __repr__(self):   # __repr__ is a special method used to represent a class's objects as a string
        return f'Block - data: {self.data}'  # __repr__ is called by the repr() built-in function


def main():  # including debug code here, so it only executes when directly call this file from cli
    block = Block('foo')
    print(block)

    print(f'block.py __name__: {__name__}')


if __name__ == '__main__':
    main()

