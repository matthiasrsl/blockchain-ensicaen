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
        first_block = Block(0, "First Block", None, datetime.now(), "<first node (unknown ip)>", branch_id=0)
        # We can reduce the format if we want to take less space
        fork_id = self.add_fork(first_block.hash, 0)
        first_block.branch_id = fork_id
        self.add_block(first_block)

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
        """
        Low-level method to add a block to the blockchain.
        Should only be called by Blockchain.new_block() and Blockchain.create_first_block().
        """
        self.blocks.add_block(block)

    def new_block(self, block_to_add):
        """
        This method is used to add a new block to the blockchain, be it created by this node
        or coming from another node.
        This method handles the creation of forks if needed.
        It should be the only place in the codebase where forks are created.
        """
        message = ""
        leaves = self.get_leaves()
        for leaf in leaves:
            block_to_add.branch_id = leaf["fork_id"]
            print(f"Block branch id: {leaf['fork_id']}")
            leaf_block = self.get_block(leaf["hash"])

            # The if and elif predicates of this condition have to be exclusive.
            # This is normally the case if is_previous is called in the predicates.
            if (  # fork case: The new bloc as a height (index) that already exists.
                    block_to_add.index == leaf_block.index
                    and block_to_add.is_valid()
                    and self.get_block(leaf_block.previous_hash).is_previous(
                block_to_add
            )
            ):

                fork_id = self.add_fork(
                    block_to_add.hash, block_to_add.index
                )
                block_to_add.branch_id = fork_id
                self.add_block(block_to_add)
                message = "****accept"  # dans ****accepte rajouter le hash ou l'index pour identifier le block
                

            elif (  # normal case: the new block's height(index) id greater that any other block's height.
                    block_to_add.is_valid()
                    and block_to_add.index == leaf_block.index + 1
                    and leaf_block.is_previous(block_to_add)
            ):
                self.add_block(block_to_add)
                self.update_fork(leaf["fork_id"], block_to_add.hash, block_to_add.index)
                message = "****accept"  # dans ****accepte rajouter le hash ou l'index pour identifier le block
            else:
                if not message:
                    message = "****refuse"

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
