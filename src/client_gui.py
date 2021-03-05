import json
from datetime import datetime

from PyQt5 import QtWidgets

import src.gui_client
from src.block import Block, BlockEncoder
from src.network import send_message


class Client(QtWidgets.QMainWindow, src.gui_client.Ui_MainWindow):
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

    def create_block(self):
        data = self.dataText.toPlainText()
        last_block = self.blockchain.get_last_block()
        block = Block(last_block.index + 1, data, last_block.hash, datetime.now())
        block.mine()
        message = "****"
        message += "mined_block|"
        message += json.dumps(block, cls=BlockEncoder)
        self.blockchain.add_block(block)
        self.handler.send_message_to_all(message)
