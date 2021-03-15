import http.server
import os
import socketserver
import sys
import threading

from src.client_terminal import Client_terminal
from src.network import NetworkHandler

VISUALIZER_PORT = 8000
LAUNCH_VISUALIZER = False

handler = NetworkHandler()


def launch_server():
    handler.start_server()
    handler.run_server()

def launch_visualizer_server():
    old_stderr = sys.stderr
    sys.stderr = open("etc/logs/visualizer.log", "a")
    sys.stderr.write("=========== NEW SESSION ============\n")

    visualizer_handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", VISUALIZER_PORT), visualizer_handler) as httpd:
        httpd.serve_forever()

    sys.stderr = old_stderr


def launch_visualizer_client():
    os.system("firefox localhost:8000/src/visualizer/visualizer.html")


if __name__ == "__main__":
    thread_server = threading.Thread(target=launch_server, daemon=True)
    thread_server.start()

    if LAUNCH_VISUALIZER:
        thread_visualiser_server = threading.Thread(target=launch_visualizer_server, daemon=True)
        thread_visualiser_server.start()

        thread_visualiser_client = threading.Thread(target=launch_visualizer_client, daemon=True)
        thread_visualiser_client.start()

    client = Client_terminal(handler)

    thread_server.join()
