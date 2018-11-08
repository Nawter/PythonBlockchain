import time
import hashlib


class Block(object):
    def __init__(self, index, proof, previous_hash, transactions, timestamp=None,actual_hash=0):
        self.index = index
        self.proof = proof
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.hash = actual_hash or self.get_block_hash

    @property
    def get_block_hash(self):
        block_string = "{}{}{}{}{}".format(self.index, self.proof, self.previous_hash, self.transactions,
                                           self.timestamp)
        return hashlib.sha256(block_string.encode()).hexdigest()

    @property
    def get_last_hash(self):
        return self.previous_hash

    def __repr__(self):
        return "{} - {} - {} - {} - {} - {}".format(self.hash,self.index, self.proof, self.previous_hash,
                                                    self.transactions,
                                                    self.timestamp)
