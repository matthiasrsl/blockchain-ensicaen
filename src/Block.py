from datetime import datetime
from hashlib import sha256

from bddBlockChain import *


class Block:

    def __init__(self, index, data, previous_hash, date):
        self.previous_hash = previous_hash
        self.index = index
        self.data = data
        self.date = date
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return sha256(f'{self.index}{self.date}{self.data}{self.previous_hash}'.encode('utf-8')).hexdigest()

    def is_previous(self, other):  # declare type block ?
        if not other.previous_hash == self.previous_hash:
            return False
        if not other.date < self.date:
            return False
        return True


def init_DB():
    return DataBaseManager("blockchain.db")


class BlockChain:

    def __init__(self):
        self.blocks = init_DB()
        self.create_first_block()  # The first block doesn't have previous hash

    def create_first_block(self):
        first_block = Block(0, "First Block", None, datetime.now())
        # We can reduce the format if we want to take less space
        self.add_block(first_block)

    def verify_blockchain(self):
        curr_index = self.get_last_block().index
        curr_block = self.get_block_at_index(curr_index)
        for i in range(curr_index - 1, -1, -1):
            prev_block = self.get_block_at_index(i)
            if not prev_block.is_previous(curr_block):
                return False
            curr_block = prev_block
        return True

    def add_block(self, block):
        self.blocks.add_block(block)

    def get_last_block(self):
        return self.blocks.getLastBlock()

    def get_block_at_index(self, index):
        return self.blocks.getBlockAtIndex(index)
