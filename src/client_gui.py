from PyQt5 import QtWidgets, QtCore

import src.gui_client
from src.network import get_local_ip, send_message


class Client(QtWidgets.QMainWindow, src.gui_client.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)
        self.setupUi(self)
        self.sendButton.clicked.connect(self.send_message)
        self.ip = get_local_ip()
        self.widget.load(
            QtCore.QUrl("http://localhost:8000/T%C3%A9l%C3%A9chargements/blockchain-visualizer/visualizer.html"))

    def send_message(self, message=None):
        if message:
            print(message)
            send_message(self.ip, message)
        else:
            message = "****"
            message += self.lineMessage.toPlainText()
            print(message)
            send_message(self.ip, message)
