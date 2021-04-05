from datetime import datetime
from unittest import TestCase

from src.db_blockchain import *


class Test(TestCase):
    def test_data_base_manager(self):
        dbmanager = DataBaseManager("testDB.db")

        dbmanager.clearDB()

        block1 = Block(1, "firstBlock", 0, datetime.now())
        block2 = Block(2, "secondBlock", 0, datetime.now())

        dbmanager.add_block(block1)
        dbmanager.add_block(block2)

        blockTest = dbmanager.getLastBlocks()[0]

        self.assertTrue(block2 == blockTest)
        self.assertTrue(block2 == dbmanager.getBlockAtIndex(2))

        dbmanager.clearDB()
