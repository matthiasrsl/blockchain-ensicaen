from PyQt5 import QtWidgets

import src.gui_start


class Client(QtWidgets.QMainWindow, src.gui_start.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)
        self.setupUi(self)
        self.show()
