import sqlite3

conn = sqlite3.connect('blockChain.db')

c=conn.cursor()

c.execute('''CREATE TABLE blocks
			 (index int,precedentHash text, hash text,data text, d date)''')

conn.commit()

conn.close()


class DataBaseManager:

	def __init__(name_data_base):
		self.name_data_base=name_data_base
		conn=sqlite3.connect(name_data_base)
		c=conn.cursor()
		c.execute('''CREATE TABLE blocks
			         (index int,precedentHash text, hash text,data text, d date)''')
		conn.commit()
		conn.close()

	def add_block(Block block):
		


