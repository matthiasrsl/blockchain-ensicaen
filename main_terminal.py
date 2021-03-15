import http.server
import os
import pathlib
import socketserver
import sys
import threading

from src.client_terminal import Client_terminal
from src.network import NetworkHandler

VISUALIZER_PORT = 8000
REDIRECT_VISUALIZER_SERVER_LOG = True
LAUNCH_VISUALIZER = True

handler = NetworkHandler()


def launch_server():
    handler.start_server()
    handler.run_server()


def launch_visualizer_server():
    if REDIRECT_VISUALIZER_SERVER_LOG:
        old_stderr = sys.stderr
        pathlib.Path("./etc/logs").mkdir(parents=True, exist_ok=True)
        sys.stderr = open("etc/logs/visualizer.log", "a")
        sys.stderr.write("=========== NEW SESSION ============\n")

    visualizer_handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", VISUALIZER_PORT), visualizer_handler) as httpd:
        httpd.serve_forever()

    if REDIRECT_VISUALIZER_SERVER_LOG:
        # noinspection PyUnboundLocalVariable
        sys.stderr = old_stderr


def init_visulizer_data():
    pathlib.Path("./etc/visudata").mkdir(parents=True, exist_ok=True)
    with open("etc/visudata/blockchain.json", "w") as file:
        file.write('''{"blockchain": []}''')


def launch_visualizer_client():
    os.system("firefox localhost:8000/src/visualizer/visualizer.html")


if __name__ == "__main__":
    init_visulizer_data()

    handler = NetworkHandler()

    thread_server = threading.Thread(target=launch_server, daemon=True)
    thread_server.start()

    if LAUNCH_VISUALIZER:
        thread_visualiser_server = threading.Thread(target=launch_visualizer_server, daemon=True)
        thread_visualiser_server.start()

        thread_visualiser_client = threading.Thread(target=launch_visualizer_client, daemon=True)
        thread_visualiser_client.start()

    client = Client_terminal(handler)

    thread_server.join()
