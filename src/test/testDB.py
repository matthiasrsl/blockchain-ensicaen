from datetime import datetime


from src.bddBlockChain import *


DataBaseManager("testDB").add_block(Block(1,"firstBlock",0,datetime.now()))


DataBaseManager("testDB").add_block(Block(2,"secondBlock",0,datetime.now()))

print(DataBaseManager("testDB").getBlockAtIndex(2))

print(DataBaseManager("testDB").getLastBlock())

