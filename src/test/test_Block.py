from unittest import TestCase

from src.Block import *


class TestBlock(TestCase):
    def test_is_previous(self):
        self.block1 = Block(1, 5, 0, datetime.now())
        self.block2 = Block(2, 5686546456, self.block1.hash, datetime.now())

        self.assertTrue(self.block1.is_previous(self.block2))
        self.assertFalse(self.block2.is_previous(self.block1))


class TestBlockChain(TestCase):
    def test_create_first_block(self):
        self.blockChain = BlockChain()

        self.assertEqual(self.blockChain.get_block_at_index(0), Block(0, "First Block", None, datetime.now()))

    def test_verify_blockchain(self):
        self.fail()
