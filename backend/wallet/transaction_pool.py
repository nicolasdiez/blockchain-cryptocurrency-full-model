class TransactionPool:
    def __init__(self):
        # the transaction pool is implemented as a dictionary (= a key-value map)
        self.transaction_map = {}

    def set_transaction(self, transaction):
        """
        Include a transaction in the transaction pool
        """
        self.transaction_map[transaction.id] = transaction

    def find_existing_transaction(self, address):
        """
        By checking the local transaction pool,
        find if there is any transaction initiated by the 'address' already in the pool
        """
        # if no transaction initiated by 'address' is found in the pool, the method implicitly returns None value
        for transaction in self.transaction_map.values():
            if transaction.input['address'] == address:
                return transaction

    def to_json_serialized(self):
        """
        Return the transactions of the pool into JSON serialized format
        """
        # get all the transaction instances from the pool
        transaction_instances = self.transaction_map.values()

        # transform the transaction instances into a list of all the JSON representations of the transaction instances
        transaction_data_json = list(map(lambda transaction: transaction.to_dictionary(), transaction_instances))

        return transaction_data_json