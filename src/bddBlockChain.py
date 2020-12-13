import sqlite3


class DataBaseManager:

	def __init__(name_data_base):
		self.name_data_base=name_data_base
		conn=sqlite3.connect(name_data_base)
		c=conn.cursor()
		c.execute('''CREATE TABLE block
			         (index int,data text, hash text, precedent_hash text, d date)''')
		conn.commit()
		conn.close()

	def add_block(Block block):
		conn=sqlite3.connect(name_data_base)
		c=conn.cursor()
		c.execute("INSERT INTO block VALUE (block.index,block.precedentHash,block.hash,block.data,block.d)")
		conn.commit()
		conn.close()


	def getBlockAtIndex(i):
		conn=sqlite3.connect(name_data_base)
		c=conn.cursor()
		c.execute("SELECT * FROM block WHERE index=?",i)
		result=c.fetchone()
		Block block(result[0],result[1],result[3],result[4])
		conn.commit()
		conn.close()
		return block

	def getLastBlock():
		conn=sqlite3.connect(name_data_base)
		c=conn.cursor()
		c.execute("SELECT MAX(index),data,hash,precedentHash,d FROM block")
		Block block(result[0],result[1],result[3],result[4])
		conn.commit()
		conn.close()
		return block


