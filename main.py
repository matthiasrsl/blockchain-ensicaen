import sys
import threading
import http.server

from PyQt5.QtWidgets import QApplication

from src.network import NetworkHandler
from src.start_gui import Start


def launch_server():
    handler = NetworkHandler()
    handler.start_server()
    handler.run_server()

def launch_visualizer():
    


if __name__ == "__main__":
    thread_server = threading.Thread(target=launch_server)
    thread_server.start()

    thread_visualiser = threading.Thread(target=launch_visualizer)
    thread_visualiser.start()

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    gui = Start()
    app.exec_()


    thread_server.join()
    thread_visualiser.join()
