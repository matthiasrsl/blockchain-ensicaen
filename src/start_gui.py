import threading

from PyQt5 import QtWidgets

import src.gui_start
from src.client_gui import Client


class Start(QtWidgets.QMainWindow, src.gui_start.Ui_MainWindow):
    def __init__(self, handler, parent=None):
        super(Start, self).__init__(parent)
        self.setupUi(self)
        self.ipLine.setText(handler.server_host)
        self.goButton.clicked.connect(self.go_button)
        self.handler = handler
        self.gui = None
        self.show()

    def go_button(self):
        self.hide()
        threading.Thread(None, self.handler_server()).start()
        threading.Thread(None, self.handler_client()).start()
        threading.Thread(None, Client(), "Client thread", self.handler.server_host)

    def handler_server(self):
        self.handler.start_server()
        self.handler.run_server()

    def handler_client(self):
        self.gui = Client(self.handler.server_host)
