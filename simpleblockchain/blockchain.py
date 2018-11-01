import block

class BlockChain(object):

    def __init__(self):
        self.chain = []
        self.current_node_transactions = []
        self.create_genesis_block()


    def create_genesis_block(self):
        pass

    def create_new_block(self, proof, previous_hash):
        pass

    def create_new_transaction(self, sender, recipient, amount):
        pass


    @staticmethod
    def create_proof_of_work(previous_proof):
        pass

    @property
    def get_last_block(self):
        return self.chain[-1]

