import json
from datetime import datetime

from PyQt5 import QtWidgets

import src.gui_ressources.gui_client
from src.block import Block, BlockEncoder
from src.network import send_message


class Client(QtWidgets.QMainWindow, src.gui_ressources.gui_client.Ui_MainWindow):
    def __init__(self, handler, parent=None):
        super(Client, self).__init__(parent)
        self.setupUi(self)
        self.sendButton.clicked.connect(self.send_message)
        self.createButton.clicked.connect(self.create_block)
        self.handler = handler
        self.blockchain = handler.blockchain

    def send_message(self, message=None):
        if message:
            print(message)
            send_message(self.ip, message)
        else:
            message = "****"
            message += self.lineMessage.toPlainText()
            self.handler.send_message_to_all(message)

    def create_block(self): # A modifier il faut qu'il puisse choisir sa branche et que les conditions dans la methode mined_block_protocol soient respecté avant de l'ajouter (add_block et add_fork)
        data = self.dataText.toPlainText()
        last_block = self.blockchain.get_last_blocks()
        block = Block(last_block[0].index + 1, data, last_block[0].hash, datetime.now())
        block.mine()
        message = "****"
        message += "mined_block|"
        message += json.dumps(block, cls=BlockEncoder)
        self.blockchain.add_block(block) #problème!
        self.blockchain.drop_fork(last_block[0].hash)
        self.blockchain.add_fork(block.hash,block.index)
        self.handler.send_message_to_all(message)
