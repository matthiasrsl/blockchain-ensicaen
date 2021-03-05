import sys
import threading

from PyQt5.QtWidgets import QApplication

from src.network import NetworkHandler
from src.start_gui import Start

handler = NetworkHandler()


def server():
    handler.start_server()
    handler.run_server()


if __name__ == "__main__":
    thread_server = threading.Thread(target=server)
    thread_server.start()
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    gui = Start(handler)
    app.exec_()
    thread_server.join()
