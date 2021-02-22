import sys

from PyQt5.QtWidgets import QApplication

from src.network import NetworkHandler
from src.start_gui import Client

if __name__ == "__main__":
    args = sys.argv
    print(args)
    handler = NetworkHandler()
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    gui = Client(handler.server_host)
    app.exec_()
    if args[1] == "server":
        handler.start_server()
        handler.run_server()
    elif args[1] == "client":
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        gui = Client(handler.server_host)
        app.exec_()
