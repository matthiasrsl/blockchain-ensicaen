import sys

from PyQt5.QtWidgets import QApplication

from src.client_gui import Client
from src.network import NetworkHandler

if __name__ == "__main__":
    args = sys.argv
    print(args)
    handler = NetworkHandler()
    if args[1] == "server":
        handler.start_server()
        handler.run_server()
    else:
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        gui = Client(args[2])
        app.exec_()
