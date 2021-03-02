from PyQt5 import QtWidgets

import src.gui_client
from src.network import get_local_ip, send_message


class Client(QtWidgets.QMainWindow, src.gui_client.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)
        self.setupUi(self)
        self.sendButton.clicked.connect(self.send_message)
        self.ip = get_local_ip()

    def send_message(self, message=None):
        if message is not None:
            send_message(self.ip, message)
        else:
            message = "****"
            message += self.lineMessage.toPlainText()
            print(message)
            send_message(self.ip, message)
