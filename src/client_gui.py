from PyQt5 import QtWidgets

import src.gui_client
from src.network import NetworkHandler, get_local_ip


class Client(QtWidgets.QMainWindow, src.gui_client.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)
        self.setupUi(self)
        self.sendButton.clicked.connect(self.send_message)
        self.ip = get_local_ip()

    def send_message(self):
        net = NetworkHandler()
        message = "****"
        message += self.lineMessage.toPlainText()
        print(message)
        net.send_message(self.ip, message)
