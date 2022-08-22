from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


def test_set_transaction():
    # create a transaction pool (to store all the transactions submitted by the blockchain nodes)
    transaction_pool = TransactionPool()

    # create a transaction of amount 100 from the sender wallet (i.e. sender address) to the recipient address
    transaction = Transaction(Wallet(), 'recipient-address', 100)

    # submit the transaction from the node to the pool
    transaction_pool.set_transaction(transaction)

    assert transaction_pool.transaction_map[transaction.id] == transaction
