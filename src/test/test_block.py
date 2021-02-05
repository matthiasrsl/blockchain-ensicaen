from unittest import TestCase
from datetime import datetime

from src.block import *


class Test(TestCase):
    def test_is_previous(self):
        self.block1 = Block(1, 5, 0, datetime.now())
        self.block2 = Block(2, 5686546456, self.block1.hash, datetime.now())

        self.assertTrue(self.block1.is_previous(self.block2))
        self.assertFalse(self.block2.is_previous(self.block1))

    def test_node_mining(self):
        self.block1 = Block(1, "Hello!", 0, datetime.now())
        self.block1.mine()

        self.assertEqual(self.block1.hash[:2], "00")
        self.assertEqual(self.block1.calculate_hash(), self.block1.hash)