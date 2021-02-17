from PyQt5 import QtWidgets

import src.GuiClient
from src.network import NetworkHandler


class Client(QtWidgets.QMainWindow, src.GuiClient.Ui_MainWindow):
    def __init__(self, ip, parent=None):
        super(Client, self).__init__(parent)
        self.ip = ip
        self.handler = NetworkHandler()

        self.setupUi(self)
        self.sendButton.clicked.connect(self.send_message)
        self.show()

    def send_message(self):
        message = "****"
        message += self.lineMessage.toPlainText()
        print(message)
        self.handler.send_message(self.ip, message)
