import http.server
import os
import socketserver
import sys
import threading

from PyQt5.QtWidgets import QApplication

from src.network import NetworkHandler
from src.start_gui import Start

VISUALIZER_PORT = 8000
REDIRECT_VISUALIZER_SERVER_LOG = True


def launch_server(handler):
    handler.start_server()
    handler.run_server()

def launch_visualizer_server():

    if REDIRECT_VISUALIZER_SERVER_LOG:
        old_stderr = sys.stderr
        sys.stderr = open("etc/logs/visualizer.log", "a")
        sys.stderr.write("=========== NEW SESSION ============\n")


    visualizer_handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", VISUALIZER_PORT), visualizer_handler) as httpd:
        httpd.serve_forever()

    if REDIRECT_VISUALIZER_SERVER_LOG:
        sys.stderr = old_stderr

def init_visulizer_data():
    with open("etc/visudata/blockchain.json", "w") as file:
        file.write('''{"blockchain": []}''')

def launch_visualizer_client():
    os.system("firefox localhost:8000/src/visualizer/visualizer.html")

if __name__ == "__main__":
    init_visulizer_data()

    handler = NetworkHandler()

    thread_server = threading.Thread(target=launch_server, args=(handler,))
    thread_server.start()

    thread_visualiser_server = threading.Thread(target=launch_visualizer_server, daemon=True)
    thread_visualiser_server.start()

    thread_visualiser_client = threading.Thread(target=launch_visualizer_client, daemon=True)
    thread_visualiser_client.start()

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    gui = Start(handler)
    app.exec_()


    thread_server.join()
