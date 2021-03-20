from datetime import datetime

from src.block import Block
from src.db_blockchain import DataBaseManager


class Blockchain:
    def __init__(self, db_name="blockchain.db", number_0=2, first=False):
        self.blocks = DataBaseManager(db_name)
        self.number_0 = number_0
        if first:
            self.create_first_block()  # The first block doesn't have previous hash

    def create_first_block(self):
        """
        Create the frist block of the blockchain
        """

        first_block = Block(
            0,
            "First Block",
            None,
            datetime.now(),
            "<first node (unknown ip)>",
            branch_id=0,
        )
        # We can reduce the format if we want to take less space
        fork_id = self.add_fork(first_block.hash, 0)
        first_block.branch_id = fork_id
        self.add_block(first_block)

    def verify_blockchain(self):
        """
        Verify that the blockchain is well chained and that block are mined
        :return: True if the blockchain is sane
        :rtype: bool
        """
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
        """
        Low-level method to add a block to the blockchain.
        Should only be called by Blockchain.new_block() and Blockchain.create_first_block().
        """
        self.blocks.add_block(block)

    def new_block(self, block):
        """
        This method is used to add a new block to the blockchain, be it created by this node
        or coming from another node.
        This method handles the creation of forks if needed.
        It should be the only place in the codebase where forks are created.
        """
        previous_block = self.get_block(block.previous_hash)
        if not (
            block.is_valid()
            and previous_block.is_previous(block)
            and block.index == previous_block.index + 1
        ):  # Block is not valid with regards to proof-of-work.
            return "****refuse"

        leaves = self.get_leaves()
        leaves_hashes = [leaf["hash"] for leaf in leaves]
        if self.nb_children(block.previous_hash) > 0:
            # The previous block is not a leaf, so we create a fork
            if block.previous_hash in leaves_hashes:
                # Just to check
                raise ValueError(
                    f"Inconsistent data: block {block.previous_hash} is "
                    "listed as a leaf but has at least one child block."
                )
            fork_id = self.add_fork(block.hash, block.index)
            block.branch_id = fork_id
            self.add_block(block)
            message = "****accept"

        else:  # The previous block is not a leaf, so we stay on the same branch
            parent_leaf = [leaf for leaf in leaves if leaf["hash"] == block.previous_hash]
            if len(parent_leaf) != 1:
                raise ValueError(
                    f"Inconsistent data: block {block.previous_hash} is "
                    "the leaf block of {len(parent_leaf)} branches (should be 1)."
                )
            parent_leaf = parent_leaf[0]
            block.branch_id = parent_leaf["fork_id"]
            self.add_block(block)
            self.update_fork(parent_leaf["fork_id"], block.hash, block.index)
            message = "****accept"

        return message

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

    def nb_children(self, hash_father):
        return self.blocks.nb_children(hash_father)

    def get_height(self):
        return self.get_last_blocks()[0].index

    def get_previous_block(self, hash_block):
        return self.get_previous_block(hash_block)

    def get_block(self, hash_block):
        return self.blocks.get_block(hash_block)

    def add_fork(self, hash_block, id):
        return self.blocks.add_fork(hash_block, id)

    def update_fork(self, fork_id, new_hash, new_height):
        self.blocks.update_fork(fork_id, new_hash, new_height)

    def drop_fork(self, hash_block):
        self.blocks.drop_fork(hash_block)

    def __del__(self):
        del self.blocks
