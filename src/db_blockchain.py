import os
import sqlite3

from src.block import *


class DataBaseManager:
    def __init__(self, name_data_base, clear=False):
        self.name_data_base = name_data_base
        if clear:
            self.clearDB()
        conn = sqlite3.connect(name_data_base)
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS blocks(id INTEGER , nonce INTEGER,
             data TEXT , hash TEXT PRIMARY KEY, precedent_hash TEXT , d DATE )"""
        )
        print("couc")
        c.execute(
            """CREATE TABLE IF NOT EXISTS forks(hash_feuille TEXT,id_feuille INTEGER , FOREIGN KEY (hash_feuille) 
            REFERENCES blocks(hash)) """
        )
        conn.commit()
        conn.close()

    def add_fork(self, hash_block, id):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        row = [
            hash_block,
            id,
        ]
        c.execute("INSERT INTO forks VALUES (?,?)", row)
        conn.commit()
        conn.close()

    def drop_fork(self, hash_block):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        c.execute("DELETE FROM forks WHERE hash_feuille=?", (hash_block,))
        conn.commit()
        conn.close()

    def add_block(self, block):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        row = [
            block.index,
            block.nonce,
            block.data,
            block.hash,
            block.previous_hash,
            block.date,
        ]
        c.execute("INSERT INTO blocks VALUES (?,?,?,?,?,?)", row)
        conn.commit()
        conn.close()

    def getBlockAtIndex(self, i):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        index = (i,)
        c.execute("SELECT * FROM blocks WHERE id=?", index)
        result = c.fetchone()
        block = Block(result[0], result[2], result[4], result[5], result[1])
        conn.commit()
        conn.close()
        return block

    def getLastBlocks(self):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        c.execute("SELECT MAX(id_feuille),hash_feuille FROM forks")
        result = c.fetchall()
        blocks = []
        for row in result:
            hash_last = row[1]
            c.execute("SELECT * FROM blocks WHERE hash=?",hash_last)
            result = c.fetchone()
            blocks.append(Block(result[0], result[1], result[3], result[4], result[5]))
        conn.commit()
        conn.close()
        return blocks

    def clearDB(self):
        try:
            os.remove(self.name_data_base)
            self.__init__(self.name_data_base)
        except FileNotFoundError:
            self.__init__(self.name_data_base)

    # Might cause bug
    # def __del__(self):
    # os.remove(self.name_data_base)
