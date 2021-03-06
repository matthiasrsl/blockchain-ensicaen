from PyQt5 import QtWidgets

import src.gui_ressources.gui_start
import src.gui_ressources.gui_start
from src.client_gui import Client
from src.network import get_local_ip


class Start(QtWidgets.QMainWindow, src.gui_ressources.gui_start.Ui_MainWindow):
    def __init__(self, handler, parent=None):
        super(Start, self).__init__(parent)
        self.setupUi(self)
        self.label.setText("You local ip is " + get_local_ip() + "\nChoose an ip to connect to:")
        self.goButton.clicked.connect(self.go_button)
        self.firstButton.clicked.connect(self.first_button)
        self.client = Client(handler)
        self.show()
        self.handler = handler

    def go_button(self):
        self.goButton.setEnabled(False)
        self.firstButton.setEnabled(False)
        self.handler.create_blockchain(False)
        self.hide()
        self.client.show()
        self.client.ip = self.ipLine.text()
        self.handler.blockchain.blocks.clearDB()
        name = self.nameLine.text()
        if name == "":
            self.handler.name = "DefaultName"
            self.client.send_message("****join|DefaultName")
        else:
            self.handler.name = name
            self.client.send_message("****join|"+name)
        

    def first_button(self):
        self.goButton.setEnabled(False)
        self.firstButton.setEnabled(False)
        self.handler.create_blockchain(True)
        self.hide()
        self.client.show()
        name = self.nameLine.text()
        if name == "":
            self.handler.name = "DefaultName"
        else:
            self.handler.name = name
        
