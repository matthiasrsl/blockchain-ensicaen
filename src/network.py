import select
import socket
import json

from src.block import Block
from src.blockchain import Blockchain


SERVER_PORT = 16385
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
        self.blockchain = Blockchain()

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
        elif message[4:9] == "join|":
            print("===== Add node")
            self.add_node(ip)
            mess = "****join_resp|"
            for ip_node in self.other_nodes:
                if ip_node != ip:
                    mess += ip_node + ","
            mess = mess[:-1]
            self.send_message(ip, mess)

            mess2 = "****blockchain|"

            last_height = message[9:]

            list_block = []
            for i in range(int(last_height), self.blockchain.get_height() + 1):
                block_json = self.blockchain.get_block_at_index(i).to_json()
                list_block.append(block_json)

            mess2 += json.dumps(list_block)

            if mess2 != "":
                self.send_message(ip, mess2)

        elif message[4:] == "leave":
            print("===== Remove node")
            self.remove_node(ip)
        elif message[4:13] == "join_resp":
            self.add_node(ip)
            ip_list = message[14:].split(",")
            for ip_node in ip_list:
                self.add_node(ip_node)
        elif message[4:] == "joined":
            print("===== Nice to meet you")
        elif message[4:] == "ack":
            print("===== Welcome")
        elif message[4:15] == "mined_block":
            block_info = message[16:].split("|")
            if block_info[2] == self.blockchain.get_last_block().hash:
                self.blockchain.add_block(
                    Block(
                        block_info[0],
                        block_info[1],
                        block_info[2],
                        block_info[3],
                    )
                )
                for ip_node in self.other_nodes:
                    self.send_message("****accept", ip_node)
            else:
                for ip_node in self.other_nodes:
                    self.send_message("****refuse", ip_node)
        elif message[4:] == "accept":
            print("===== Node accepted")
        elif message[4:] == "refuse":
            print("===== Node refused")

        elif message[4:14] == "blockchain":

            blockchain = json.loads(message[15:])

            for block in blockchain:
                self.blockchain.add_block(Block(**block))

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
