from datetime import datetime

from src.Block import Block
from src.bddBlockChain import DataBaseManager


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
            if not curr_block.is_valid():
                return False
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

    def get_height(self):
        return self.get_last_block().index
