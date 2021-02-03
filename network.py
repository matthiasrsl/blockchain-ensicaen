import socket
import select


SERVER_PORT = 1501
CLIENT_PORT = 1500
RECV_SIZE = 1024
LISTEN_TIME = 5


class Node:
    def __init__(self, ip_address):
        self.ip_address = ip_address


class NetworkHandler:
    def __init__(self):
        self.other_nodes = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_clients = []

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.server_host = s.getsockname()[0]
        s.close()

        # self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.keep_running_server = True

    def start_server(self):
        self.server.bind((self.server_host, SERVER_PORT))
        self.server.listen(5)

    def send_message(self, ip, message):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((ip, SERVER_PORT))
        print("Client Connected")
        message = message.encode()
        connection.send(message)
        connection.close()

    def add_node(self, ip):
        node = Node(ip)
        self.other_nodes[ip] = node

    def remove_node(self, ip):
        try:
            del self.other_nodes[ip]
        except KeyError:
            print(f"{ip} tried to be removed but not in list")

    def process_message(self, message, ip):
        print(f"Received: {message}")

        if message[:4] != "****":
            print("Error: bad request")
        elif message[4] == "1":
            print("===== Add node")
            self.add_node(ip)
        elif message[4] == "2":
            print("===== Remove node")
            self.remove_node(ip)
        else:
            print("Error: bad request")

        print(f"Other nodes: {self.other_nodes}")

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
                    ip, port = client.getpeername()
                    message = message.decode()
                    self.process_message(message, ip)
                    self.connected_clients.remove(client)
                    client.close()

        for client in self.connected_clients:
            client.close()
