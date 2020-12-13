from datetime import datetime
from hashlib import sha256


class Block:

    def __init__(self, index, data, precedent_hash, date):
        self.precedentHash = precedent_hash
        self.hash = self.calculate_hash()
        self.index = index
        self.data = data
        self.date = date

    def calculate_hash(self):
        return sha256(self).hexdigest()


class BlockChain:

    def __init__(self):
        self.blocks = self.init_DB()
        self.create_first_block()  # The first block doesn't have previous hash

    def create_first_block(self):
        first_block = Block(0, "First Block", None, datetime.now())
        # We can reduce the format if we want to take less space
        self.add_block(first_block)

    def add_block(self, block):
        
    def init_DB(self):
