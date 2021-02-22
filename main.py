import sys

from PyQt5.QtWidgets import QApplication

from src.network import NetworkHandler
from src.start_gui import Start

if __name__ == "__main__":
    args = sys.argv
    print(args)
    handler = NetworkHandler()
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    gui = Start(handler)
    app.exec_()
