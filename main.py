import sys
import threading
import http.server
import socketserver
import os

from PyQt5.QtWidgets import QApplication

from src.network import NetworkHandler
from src.start_gui import Start

VISUALIZER_PORT = 8000

def launch_server():
    handler = NetworkHandler()
    handler.start_server()
    handler.run_server()

def launch_visualizer_server():
    visualizer_handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", VISUALIZER_PORT), visualizer_handler) as httpd:
        httpd.serve_forever()

def launch_visualizer_client():
    os.system("firefox localhost:8000/src/visualizer/visualizer.html")

if __name__ == "__main__":
    thread_server = threading.Thread(target=launch_server)
    thread_server.start()

    thread_visualiser_server = threading.Thread(target=launch_visualizer_server, daemon=True)
    thread_visualiser_server.start()

    thread_visualiser_client = threading.Thread(target=launch_visualizer_client, daemon=True)
    thread_visualiser_client.start()

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    gui = Start()
    app.exec_()


    thread_server.join()
