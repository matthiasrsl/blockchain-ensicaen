import json
import threading
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
        handler.client = self
        self.hiddenRefreshButton.setVisible(False)
        self.name = None #useless

        self.sendButton.clicked.connect(self.send_message)
        self.createButton.clicked.connect(self.create_block)
        self.manuelBox.stateChanged.connect(self.check_receive)
        self.acceptBox.accepted.connect(self.handler.accept_mined_block)
        self.acceptBox.rejected.connect(self.handler.refuse_mined_block)
        self.hiddenRefreshButton.clicked.connect(self.set_displayer_text)
        self.leaveButton.clicked.connect(self.leave)
        self.joinButton.clicked.connect(self.join)

    def send_message(self, message=None):
        """
        Send message, if there is an argument, it send to the ip attribut, else it send to all
        the message is then taken from the GUI
        :param message: A message to send
        :type message: String
        """
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

    def create_block(self):
        """
        Create a block from what is typed in the GUI, mine it and send it
        """
        data = self.dataText.toPlainText()
        last_block = self.handler.blockchain.get_last_blocks()
        block = Block(last_block[0].index + 1, data, last_block[0].hash, datetime.now(),str(self.handler.server_host))
        block.mine(number_0=self.handler.blockchain.number_0)
        message = "****"
        message += "mined_block|"
        message += json.dumps(block, cls=BlockEncoder)
        self.handler.blockchain.new_block(block)
        self.handler.send_message_to_all(message)
        message_dict = {"sender": "Me", "content": message}
        self.handler.message_list.append(message_dict)

    def check_receive(self):
        self.acceptBox.setEnabled(self.manuelBox.isChecked())
        self.handler.manual_validation = self.manuelBox.isChecked()

    def set_displayer_text(self):
        self.blockDisplayer.setText(str(self.handler.block_to_add))

    def leave(self):
        self.handler.send_message_to_all("****leave")
        self.handler.other_nodes = {}
        self.joinButton.setEnabled(True)
        self.ipLine.setEnabled(True)
        self.leaveButton.setEnabled(False)

    def join(self):
        send_message(self.ipLine.text(), "****join|" + str(self.handler.blockchain.get_real_last_block().index+1))
        self.leaveButton.setEnabled(True)
        self.ipLine.setEnabled(False)
        self.joinButton.setEnabled(False)

    def closeEvent(self, event):
        self.handler.send_message_to_all("****leave")
        message_dict = {"sender": "Me", "content": "****leave"}
        self.handler.message_list.append(message_dict)
        exit()
