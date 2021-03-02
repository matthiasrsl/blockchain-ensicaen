from PyQt5 import QtWidgets

import src.gui_start
import src.gui_start
from src.client_gui import Client
from src.network import get_local_ip


class Start(QtWidgets.QMainWindow, src.gui_start.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Start, self).__init__(parent)
        self.setupUi(self)
        self.label.setText("You local ip is "+get_local_ip()+"\nChoose an ip to connect to")
        self.ipLine.setText(get_local_ip())
        self.goButton.clicked.connect(self.go_button)
        self.client = Client()
        self.show()

    def go_button(self):
        self.hide()
        self.client.show()
