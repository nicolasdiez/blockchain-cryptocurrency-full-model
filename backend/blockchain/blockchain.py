from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.config import MINING_REWARD_INPUT_ADDRESS


class Blockchain:
    """
    Blockchain: is a public ledger of transactions, implemented as a linked list of Blocks.
    """

    def __init__(self):
        # first block of the chain is always the genesis block
        self.chain = [Block.genesis()]

    def __repr__(self):  # method to print the Blockchain object as string
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

        # 1
        if chain[0] != Block.genesis():
            raise Exception('The genesis block is not correct')

        # 2 validate every block, except for the 1st one (i.e. the genesis block)
        for i in range(1, len(chain)):
            current_block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, current_block)

    @staticmethod
    def is_valid_chain_transactions(chain):
        """
        Validate a chain of blocks from the point of view of the transactions included on it.
        Conditions that must be met are the following:
        1- each transaction must appear only once within the chain
        2- only one mining reward is permited per block
        3- each transaction must comply with the transaction rules
        """

        transactions_ids_in_chain = set()

        for block in chain:
            block_has_mining_reward = False
            
            for transacion_dict in block.data:
                transaction = Transaction.from_dictionary(transacion_dict)

                if transaction.input == MINING_REWARD_INPUT_ADDRESS:
                    if block_has_mining_reward:
                        raise Exception(f'Block with hash {block.hash} has more than one mining reward. Only 1 mining reward is allowed per block')
                    
                    block_has_mining_reward = True

                if transaction.id in transactions_ids_in_chain:
                    raise Exception(f'Transaction {transaction.id} is not unique in the chain')
                
                transactions_ids_in_chain.add(transaction.id)

                Transaction.is_valid_transaction(transaction)

    def replace_chain(self, incoming_chain):
        """
        Replace the local copy of the chain with the incoming chain broadcasted by the rest of the network nodes.
        The local chain is replaced if all these conditions are met:
        1- The incoming chain is longer than the local chain
        2- The incoming chain is a valid chain regarding its formatting
        """

        # 1
        if len(incoming_chain) <= len(self.chain):
            raise Exception('Can not replace the local chain. The incoming chain must be longer')

        # 2
        try:
            Blockchain.is_valid_chain(incoming_chain)
        except Exception as exception:
            raise Exception(f'Can not replace the local chain. The incoming chain must be valid: {exception}')

        # if conditions 1 and 2 are met, replace the local copy of the chain with the incoming broadcasted chain
        self.chain = incoming_chain

    def to_list(self):
        """
        Transform the blockchain into a list of blocks
        """
        chain_list = []

        for i_block in self.chain:
            chain_list.append(i_block.to_dictionary())

        return chain_list

        # return list(map(lambda block: block.to_dictionary(), self.chain))

    @staticmethod
    def from_list(chain_list):
        """
         Transform a list of blocks into an actual blockchain instance
         """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block_dictionary: Block.from_dictionary(block_dictionary), chain_list))

        return blockchain


def main():  # including debug code here, so it only executes when directly calling this file from cli
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)
    print(f'blockchain.py __name__: {__name__}')


if __name__ == '__main__':
    main()