from Block import *
import sqlite3


class DataBaseManager:

    def __init__(self, name_data_base):
        self.name_data_base = name_data_base
        conn = sqlite3.connect(name_data_base)
        c = conn.cursor()
        c.execute('''CREATE TABLE block(index int,data text, hash text, precedent_hash text, d date)''')
        conn.commit()
        conn.close()

    def add_block(self, block):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        c.execute("INSERT INTO block VALUE (block.index,block.precedentHash,block.hash,block.data,block.d)")
        conn.commit()
        conn.close()

    def getBlockAtIndex(self, i):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        c.execute("SELECT * FROM block WHERE index=?", i)
        result = c.fetchone()
        block = Block(result[0], result[1], result[3], result[4])
        conn.commit()
        conn.close()
        return block

    def getLastBlock(self):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        result = c.execute("SELECT MAX(index),data,hash,precedentHash,d FROM block")
        block = Block(result[0], result[1], result[3], result[4])
        conn.commit()
        conn.close()
        return block
