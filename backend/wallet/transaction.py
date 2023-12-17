import uuid
import time

from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD, MINING_REWARD_INPUT_ADDRESS


class Transaction:
    """
    A Transaction is a written proof of a currency exchange between one sender and one or more recipients
    Considerations of a Transaction:
    - Only 1 transaction per sender per block
    - A transaction can contain multiple recipients
    """
    # set all the input values to default value None
    def __init__(self, sender_wallet=None, recipient_address=None, amount=None, id=None, output=None, input=None):

        # 'id' is used if provided into the object instantiation, otherwise use the random UUID
        self.id = id or str(uuid.uuid4())[:8]

        # 'output' is used if provided into the object instantiation, otherwise use the generate method
        self.output = output or self.generate_output_balance(sender_wallet, recipient_address, amount)

        # 'input' is used if provided into the object instantiation, otherwise use the generate method
        self.input = input or self.generate_transaction(sender_wallet, self.output)

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
        Override an existing transaction for an existing or new recipient
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
        Verifies if a transaction is correct in terms of structure.
        """
        # Transactions which are mining rewards comply with: 
        # 1. As output they have just one single entry
        # 2. The value output is equal to the MINING_REWARD value
        if (transaction.input == MINING_REWARD_INPUT_ADDRESS):
            if len(transaction.output) != 1:
                raise Exception('Error - Minining reward is not valid: transaction output has more than 1 recipient')
            
            output_values = list(transaction.output.values())
            if output_values != [MINING_REWARD]:
                raise Exception('Error - Minining reward is not valid: transaction output value is not equal to MINING_REWARD value')
            
            return

        # Transaction output total amount must be equal to the input amount
        output_total_balance = sum(transaction.output.values())

        if transaction.input['amount'] != output_total_balance:
            raise Exception('Error in the output transaction balance')

        # Transaction signature must be correct
        if not Wallet.verify_signature(transaction.input['public_key'], transaction.output,
                                       transaction.input['signature']):
            raise Exception('Error in transaction signature')

    @staticmethod
    def generate_mining_reward_transaction(miner_wallet: Wallet):
        """
        Create a new reward transaction for the miner
        """
        output_reward_transaction = {miner_wallet.address: MINING_REWARD}

        return Transaction(input=MINING_REWARD_INPUT_ADDRESS, output=output_reward_transaction)

    def to_dictionary(self):
        """
        Transform an actual transaction instance into a dictionary which contains its attributes (= JSON)
        """
        return self.__dict__

    @staticmethod
    def from_dictionary(transaction_dictionary):
        """
        Transform a dictionary containing transaction attributes (= JSON) back into an actual transaction instance
        """
        return Transaction(**transaction_dictionary)
    

def main():
    transaction = Transaction(Wallet(), 'recipient', 15)
    print(f'transaction.__dict__:{transaction.__dict__}')

    transaction_dictionary = transaction.to_dictionary()
    restored_transaction = Transaction.from_dictionary(transaction_dictionary)
    print(f'restored_transaction.__dict__:  {restored_transaction.__dict__}')


if __name__ == '__main__':
    main()