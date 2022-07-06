import uuid
import time

from backend.wallet.wallet import Wallet


class Transaction:
    """
    Written proof of a currency exchange between one sender and one or more recipients
    Considerations of a Transaction:
    - Only 1 transaction per sender per block
    - A transaction can contain multiple recipients
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

    def update_transaction(self, sender_wallet, recipient_address, amount):
        """
        Override an existing transaction for an existing or a new recipient
        """

        if amount > self.output[sender_wallet.address]:
            raise Exception("Amount exceeds sender's balance")

        # if the recipient is an existing one
        if recipient_address in self.output:
            self.output[recipient_address] = self.output[recipient_address] + amount
        # if the recipient is a new one
        else:
            self.output[recipient_address] = amount

        # update the sender´s wallet balance in the output balance structure
        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount

        # because the output final balance has changed due to the update, the transaction has to be signed again
        self.input = self.generate_transaction(sender_wallet, self.output)

    @staticmethod
    def is_valid_transaction(transaction):
        """
        Verifies is a transaction is correct in terms of structure.
        """
        output_total_balance = sum(transaction.output.values())

        if transaction.input['amount'] != output_total_balance:
            raise Exception('Error in the output transaction balance')

        if not Wallet.verify_signature(transaction.input['public_key'], transaction.output,
                                       transaction.input['signature']):
            raise Exception('Error in transaction signature')

    def to_dictionary(self):
        """
        Transform the transaction into a dictionary which contains its attributes
        """
        return self.__dict__


def main():
    transaction = Transaction(Wallet(), 'recipient', 15)
    print(f'transaction.__dict__:{transaction.__dict__}')


if __name__ == '__main__':
    main()