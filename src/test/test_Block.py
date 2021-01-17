from unittest import TestCase
from datetime import datetime
from src.Block import *


class Test(TestCase):
    def test_is_previous(self):
        self.block1 = Block(1, 5, 0, datetime.now())
        self.block2 = Block(2, 5686546456, self.block1.hash, datetime.now())

        self.assertTrue(self.block1.is_previous(self.block2))
        self.assertFalse(self.block2.is_previous(self.block1))
