from unittest import TestCase
from src.BlockChain import *
from src.Block import *


class Test(TestCase):
    def test_block_chain(self):
        blockchain = BlockChain()
        block1 = Block(1, "useless", blockchain.get_last_block().hash, datetime.now())
        blockchain.add_block(block1)
        block2 = Block(1, "useless", block1.hash, datetime.now())
        blockchain.add_block(block2)
        block3 = Block(1, "useless", block2.hash, datetime.now())
        blockchain.add_block(block3)
        self.assertTrue(blockchain.verify_blockchain())
