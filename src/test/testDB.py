from src.Block import *
import sqlite3
from src.bddBlockChain import *


DataBaseManager("testDB").add_block(Block(1,"firstBlock",0,datetime.now()))

