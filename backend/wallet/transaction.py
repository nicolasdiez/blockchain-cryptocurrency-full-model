import uuid
import time

from backend.wallet.wallet import Wallet


class Transaction:
    """
    Written proof of a currency exchange between one sender and one or more recipients
    """

    def __init__(self, sender_wallet, recipient_address, amount):
        self.id = str(uuid.uuid4())[:8]
        self.output = self.generate_output_balance(sender_wallet, recipient_address, amount)

        self.input = self.generate_transaction(sender_wallet, self.output)

    @staticmethod
    def generate_output_balance(sender_wallet, recipient_address, amount):
        """
        Create a structure with the output balance data representing the transaction.
        The structure holds the balance amount of the sender and recipient after the transaction is completed.
        """

        if amount > sender_wallet.balance:
            raise Exception("Amount exceeds sender's balance")

        output = {}
        output[recipient_address] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount

        return output

    @staticmethod
    def generate_transaction(sender_wallet, output_balance):
        """
        Create a structure summarizing all the data involved in the transaction, that is:
        - timestamp of the transaction
        - balance amount of the sender before the transaction
        - wallet address of the sender
        - public key of the sender
        - signature: which at the same time includes the final balance amount for sender and recipient after transaction
        """
        return {
            'timestamp': time.time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output_balance)
        }


def main():
    transaction = Transaction(Wallet(), 'recipient', 15)
    print(f'transaction.__dict__:{transaction.__dict__}')


if __name__ == '__main__':
    main()