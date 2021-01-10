import socket
import select

SERVER_HOST = "localhost"
SERVER_PORT = 1500
CLIENT_PORT = 1501
RECV_SIZE = 1024
LISTEN_TIME = 0.05


class Node:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # This is the client socket used to send information to the node.


class NetworkHandler:
    def __init__(self, hostname):
        self.hostname = hostname
        self.other_nodes = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_clients = []

        # self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.keep_running_server = True

    def start_server(self):
        self.server.bind((SERVER_HOST, SERVER_PORT))
        self.server.listen(5)

    def send_message(self, message):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((self.hostname, SERVER_PORT))
        print("Client Connected")
        message = message.encode()
        connection.send(message)
        connection.close()

    def run_server(self):
        while self.keep_running_server:
            incoming_connections, wlist, xlist = select.select(
                [self.server], [], [], LISTEN_TIME
            )

            for connection in incoming_connections:
                client_connection, client_connection_info = connection.accept()
                self.connected_clients.append(client_connection)

            clients_to_be_read = []
            try:
                clients_to_be_read, wlist, xlist = select.select(
                    self.connected_clients, [], [], LISTEN_TIME
                )
            except select.error:
                print("error")
            else:
                for client in clients_to_be_read:
                    message = client.recv(RECV_SIZE)
                    message = message.decode()
                    print(f"Received: {message}")
                    self.connected_clients.remove(client)
                    client.close()
                    if message == "stop":
                        self.keep_running_server = False

        for client in self.connected_clients:
            client.close