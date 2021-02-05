from unittest import TestCase

from src.blockchain import *
from src.block import *


class Test(TestCase):
    def test_block_chain(self):
        blockchain = Blockchain("testdb.db", clear=True)
        block1 = Block(
            1, "useless", blockchain.get_last_block().hash, datetime.now()
        )
        block1.mine()
        blockchain.add_block(block1)
        block2 = Block(2, "useless", block1.hash, datetime.now())
        block2.mine()
        blockchain.add_block(block2)
        block3 = Block(3, "useless", block2.hash, datetime.now())
        block3.mine()
        blockchain.add_block(block3)
        self.assertTrue(blockchain.verify_blockchain())
