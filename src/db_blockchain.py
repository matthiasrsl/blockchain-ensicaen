import os
import sqlite3
import pathlib

from src.block import *


class DataBaseManager:
    def __init__(self, name_data_base, clear=True):
        self.name_data_base = name_data_base
        try:
            os.remove(self.name_data_base)
        except FileNotFoundError:
            pass  # We juste want the file to not be present.
        conn = sqlite3.connect(name_data_base)
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS blocks(id INTEGER , nonce INTEGER,
             data TEXT , hash TEXT PRIMARY KEY, precedent_hash TEXT , d DATE, miner TEXT, branch_id INTEGER )"""
        )
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

        c.execute("SELECT rowid FROM forks WHERE hash_feuille=?", (hash_block,))
        fork_id = c.fetchone()[0]
        print(f"fork id: {fork_id}")
        conn.close()

        return fork_id

    def update_fork(self, fork_id, new_hash, new_height):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        data = (new_hash, new_height, fork_id)
        c.execute("UPDATE forks SET hash_feuille=?, id_feuille=? WHERE rowid=?", data)
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
            block.miner,
            block.branch_id
        ]
        try:
            c.execute("INSERT INTO blocks VALUES (?,?,?,?,?,?,?,?)", row)
        except sqlite3.IntegrityError:
            print("Error block already in blockchain")
        conn.commit()
        conn.close()
        self.updateVisualizer()

    def getBlockAtIndex(self, index):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        c.execute("SELECT * FROM blocks WHERE id=?", (index,))
        result = c.fetchone()
        block = Block(result[0], result[2], result[4], result[5], result[1])
        conn.commit()
        conn.close()
        return block

    def getLastBlocks(self):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        c.execute("SELECT MAX(id_feuille),hash_feuille FROM forks")  # pour ??tre a l'abris des collisions ont peut
        # ??galement verifier les indexs
        result = c.fetchall()
        blocks = []
        for row in result:
            hash_last = row[1]
            c.execute("SELECT id ,data  , precedent_hash , d, miner, nonce FROM blocks WHERE hash=?", (hash_last,))
            result = c.fetchone()
            blocks.append(Block(result[0], result[1], result[2], result[3], result[4],result[5]))
        conn.commit()
        conn.close()
        return blocks

    def get_previous_block(self,
                           hash_block):  # au final pas tr??s utile une fonction qui retourn un block en fontcion de son hash suffit
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        c.execute("SELECT precedent_hash FROM blocks WHERE hash=?",
                  (hash_block,))  # pour ??tre a l'abris des collisions ont peut ??galement verifier les indexs
        result = c.fetchone()
        c.execute("SELECT id ,data , precedent_hash , d, miner, nonce, branch_id FROM blocks WHERE hash=?",
                  (result,))  # pour ??tre a l'abris des collisions ont peut ??galement verifier les indexs
        result = c.fetchone()
        block = (Block(result[0], result[1], result[2], result[3], result[4], result[5], branch_id=result[6]))
        conn.commit()
        conn.close()
        return block

    def get_block(self, hash_block):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        c.execute("SELECT id , data ,precedent_hash , d, miner, nonce, branch_id  FROM blocks WHERE hash=?",
                  (hash_block,))
        result = c.fetchone()
        block = None
        if result != None:
            block = (Block(result[0], result[1], result[2], result[3], result[4], result[5], branch_id=result[6]))
        conn.commit()
        conn.close()
        return block

    def get_all_blocks(self):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        c.execute("SELECT * FROM blocks")
        blocks_raw = c.fetchall()
        blocks = [Block(result[0], result[2], result[4], result[5], result[6], result[1], branch_id=result[7]) for result in blocks_raw]
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
        pathlib.Path("./etc/visudata/").mkdir(parents=True, exist_ok=True)
        with open("etc/visudata/blockchain.json", "w") as file:
            file.write(blockchain_json)

    def get_leaves(self):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        c.execute("SELECT rowid,* FROM forks")
        result = c.fetchall()
        leaves = []
        for row in result:
            leaves.append({"hash": row[1], "id": row[2], "fork_id": row[0]})
        conn.commit()
        conn.close()
        return leaves

    def nb_children(self, hash_father):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        c.execute("SELECT hash FROM blocks WHERE precedent_hash=?", (hash_father,))
        result = c.fetchall()
        conn.commit()
        conn.close()
        return len(result)

    def is_empty(self):
        conn = sqlite3.connect(self.name_data_base)
        c = conn.cursor()
        c.execute("SELECT * FROM blocks")
        result = c.fetchall()
        conn.commit()
        conn.close()
        return len(result) == 0

    def clearDB(self):
        try:
            os.remove(self.name_data_base)
            self.__init__(self.name_data_base, clear=False)
        except FileNotFoundError:
            self.__init__(self.name_data_base, clear=False)

    # Might cause bug
    # def __del__(self):
    # os.remove(self.name_data_base)
