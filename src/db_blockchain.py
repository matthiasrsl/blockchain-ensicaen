import os
import sqlite3
import json

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
             data TEXT , hash TEXT , precedent_hash TEXT , d DATE )"""
        )
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
        self.updateVisualizer()

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

    def get_all_blocks(self):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        c.execute("SELECT * FROM blocks")
        blocks_raw = c.fetchall()
        blocks = [Block(result[0], result[2], result[4], result[5], result[1]) for result in blocks_raw]
        conn.commit()
        conn.close()
        return blocks

    def updateVisualizer(self):
        blocks_raw = self.get_all_blocks()
        blocks = []
        for block in blocks_raw:
            try:
                block.data = json.loads(block.data)
            except json.decoder.JSONDecodeError:
                block.data = block.data
            blocks.append(block)
            
        blockchain = {"blockchain": blocks}
        blockchain_json = json.dumps(blockchain, cls=BlockEncoder)
        with open("etc/visudata/blockchain.json", "w") as file:
            file.write(blockchain_json)

    def clearDB(self):
        try:
            os.remove(self.name_data_base)
            self.__init__(self.name_data_base)
        except FileNotFoundError:
            self.__init__(self.name_data_base)

    #Might cause bug
    #def __del__(self):
        #os.remove(self.name_data_base)
