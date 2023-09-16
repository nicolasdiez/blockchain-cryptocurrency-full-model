from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain


def test_set_transaction():
    # create a transaction pool (to store all the transactions submitted by the blockchain nodes)
    transaction_pool = TransactionPool()

    # create a transaction of amount 100 from the sender wallet (i.e. sender address) to the recipient address
    transaction = Transaction(Wallet(), 'recipient-address', 100)

    # submit the transaction from the node to the pool
    transaction_pool.set_transaction(transaction)

    assert transaction_pool.transaction_map[transaction.id] == transaction


def test_clear_transactions():
    # create a transaction pool (to store all the transactions submitted by the blockchain nodes)
    transaction_pool = TransactionPool()

    # create a transaction of amount 100 from the sender wallet (i.e. sender address) to the recipient address
    transaction_1 = Transaction(Wallet(), 'recipient-address', 100)

    # create a transaction of amount 200 from the sender wallet (i.e. sender address) to the recipient address
    transaction_2 = Transaction(Wallet(), 'recipient-address', 200)

    # add the transactions to the pool
    transaction_pool.set_transaction(transaction_1)
    transaction_pool.set_transaction(transaction_2)

    # create a chain and add the transactions to the block
    blockchain = Blockchain()
    blockchain.add_block([transaction_1.to_dictionary(), transaction_2.to_dictionary()])

    # make sure the transactions are actually present into the pool
    assert transaction_1.id in transaction_pool.transaction_map
    assert transaction_2.id in transaction_pool.transaction_map

    # clear transactions from the pool
    transaction_pool.clear_transactions(blockchain)

    # make sure the transactions are actually not present into the pool anymore
    assert not transaction_1.id in transaction_pool.transaction_map
    assert not transaction_2.id in transaction_pool.transaction_map