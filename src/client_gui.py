import json
from datetime import datetime

from PyQt5 import QtWidgets

import src.gui_ressources.gui_client
from src.block import Block, BlockEncoder
from src.network import send_message, NetworkHandler


class Client(QtWidgets.QMainWindow, src.gui_ressources.gui_client.Ui_MainWindow):
    def __init__(self, handler: NetworkHandler, parent=None):
        super(Client, self).__init__(parent)
        self.setupUi(self)
        self.handler = handler
        self.blockchain = handler.blockchain
        handler.client = self
        self.hiddenRefreshButton.setVisible(False)

        self.sendButton.clicked.connect(self.send_message)
        self.createButton.clicked.connect(self.create_block)
        self.manuelBox.stateChanged.connect(self.check_receive)
        self.acceptBox.accepted.connect(self.handler.accept_mined_block)
        self.acceptBox.rejected.connect(self.handler.refuse_mined_block)
        self.hiddenRefreshButton.clicked.connect(self.set_displayer_text)

    def send_message(self, message=None):
        if message:
            print(message)
            send_message(self.ip, message)
            message_dict = {"sender": "Me", "content": message}
            self.handler.message_list.append(message_dict)
        else:
            message = "****"
            message += self.lineMessage.toPlainText()
            self.handler.send_message_to_all(message)
            message_dict = {"sender": "Me", "content": message}
            self.handler.message_list.append(message_dict)

    def create_block(self):  # A modifier il faut qu'il puisse choisir sa branche et que les conditions dans la methode
        # mined_block_protocol soient respecté avant de l'ajouter (add_block et add_fork)
        data = self.dataText.toPlainText()
        last_block = self.blockchain.get_last_blocks()
        block = Block(last_block[0].index + 1, data, last_block[0].hash, datetime.now())
        block.mine()
        message = "****"
        message += "mined_block|"
        message += json.dumps(block, cls=BlockEncoder)
        self.blockchain.add_block(block)  # problème!
        self.blockchain.add_fork(block.hash, block.index)
        self.handler.send_message_to_all(message)
        message_dict = {"sender": "Me", "content": message}
        self.handler.message_list.append(message_dict)

    def check_receive(self):
        self.acceptBox.setEnabled(self.manuelBox.isChecked())
        self.handler.manual_validation = self.manuelBox.isChecked()

    def set_displayer_text(self):
        self.blockDisplayer.setText(str(self.handler.block_to_add))
