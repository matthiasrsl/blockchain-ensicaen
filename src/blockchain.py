from datetime import datetime

from src.block import Block
from src.db_blockchain import DataBaseManager


class Blockchain:
    def __init__(self, db_name="blockchain.db", number_0=2, clear=False):
        self.blocks = DataBaseManager(db_name, clear=clear)
        self.number_0 = number_0
        if clear is not False:
            self.create_first_block()  # The first block doesn't have previous hash

    def create_first_block(self):
        first_block = Block(0, "First Block", None, datetime.now())
        # We can reduce the format if we want to take less space
        self.add_block(first_block)
        self.add_fork(first_block.hash, 0)

    def verify_blockchain(self):
        curr_index = self.get_last_blocks()[0].index
        curr_block = self.get_block_at_index(curr_index)
        for i in range(curr_index - 1, -1, -1):
            prev_block = self.get_block_at_index(i)
            if not curr_block.is_valid(number_0=self.number_0):
                return False
            if not prev_block.is_previous(curr_block):
                return False
            curr_block = prev_block
        return True

    def add_block(self, block):
        self.blocks.add_block(block)

    def get_last_blocks(self):
        return self.blocks.getLastBlocks()

    def get_real_last_block(self):
        list_block = self.get_last_blocks()
        last_block = list_block[0]

        for block in list_block:
            if last_block.date < block.date:
                last_block = block

        return last_block

    def get_leaves(self):
        return self.blocks.get_leaves()

    def get_block_at_index(self, index):
        return self.blocks.getBlockAtIndex(index)

    def get_height(self):
        return self.get_last_blocks()[0].index

    def get_previous_block(self, hash_block):
        return self.get_previous_block(hash_block)

    def get_block(self, hash_block):
        return self.blocks.get_block(hash_block)

    def add_fork(self, hash_block, id):
        self.blocks.add_fork(hash_block, id)

    def drop_fork(self, hash_block):
        self.blocks.drop_fork(hash_block)

    def __del__(self):
        del self.blocks
