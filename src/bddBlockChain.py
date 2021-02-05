from src.Block import *
import sqlite3
import os


class DataBaseManager:

    def __init__(self, name_data_base):
        self.name_data_base = name_data_base
        conn = sqlite3.connect(name_data_base)
        c = conn.cursor()
        c.execute(
            '''CREATE TABLE IF NOT EXISTS blocks(id INTEGER , nonce INTEGER,
             data TEXT , hash TEXT , precedent_hash TEXT , d DATE )''')
        conn.commit()
        conn.close()

    def add_block(self, block):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        row = [block.index, block.nonce, block.data, block.hash, block.previous_hash, block.date]
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

    def getLastBlock(self):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        c.execute("SELECT MAX(id),data,hash,precedent_hash,d,nonce FROM blocks")
        result = c.fetchone()
        block = Block(result[0], result[1], result[3], result[4], result[5])
        conn.commit()
        conn.close()
        return block

    def clearDB(self):
        os.remove(self.name_data_base)
        self.__init__(self.name_data_base)
