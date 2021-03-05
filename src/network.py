import json
import select
import socket

from src.block import Block, BlockEncoder
from src.blockchain import Blockchain

SERVER_PORT = 16385
RECV_SIZE = 1024
LISTEN_TIME = 5


class Node:
    def __init__(self, ip_address):
        self.ip_address = ip_address


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    server_host = s.getsockname()[0]
    s.close()
    return server_host


def send_message(ip, message):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((ip, SERVER_PORT))
    print("Client Connected")
    message = message.encode()
    connection.send(message)
    connection.close()


class NetworkHandler:
    def __init__(self):
        self.other_nodes = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_clients = []
        self.blockchain = Blockchain()

        self.server_host = get_local_ip()

        # self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.keep_running_server = True

    def start_server(self):
        self.server.bind((self.server_host, SERVER_PORT))
        self.server.listen(5)

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
        elif message.split("|")[0][4:] == "join":
            self.join_protocol(ip, message)

        elif message[4:] == "leave":
            print("===== Remove node")
            self.remove_node(ip)

        elif message.split("|")[0][4:] == "join_resp":
            self.join_resp_protocol(ip, message)

        elif message[4:] == "joined":
            self.add_node(message.split("|")[1])
            print("===== Nice to meet you")

        elif message[4:] == "ack":
            print("===== Welcome")

        elif message.split("|")[0][4:] == "mined_block":
            self.mined_block_protocol(message)

        elif message[4:] == "accept":
            print("===== Node accepted")

        elif message[4:] == "refuse":
            print("===== Node refused")

        elif message.split("|")[0][4:] == "blockchain":
            self.blockchain_protocol(message)

        elif message.split("|")[0][4:] == "ackdefault":
            print("==== This node may be defective")

        else:
            print("Error: bad request")

        print(f"Other nodes: {self.other_nodes}")

    def blockchain_protocol(self, message):
        blockchain = json.loads(message.split("|")[1])
        for block in blockchain:
            self.blockchain.add_block(Block(**block))

    def mined_block_protocol(self, message):
        block_info = message.split("|")
        block_to_add = Block(block_info[0], block_info[1], block_info[2], block_info[3])
        if block_to_add.is_valid() and block_to_add.is_previous(
            self.blockchain.get_last_block()
        ):
            self.blockchain.add_block(block_to_add)

            for ip_node in self.other_nodes:
                send_message(
                    ip_node, "****accept"
                )  # dans ****accepte rajouter le hash ou l'index pour identifier le block
        else:
            for ip_node in self.other_nodes:
                send_message(ip_node, "****refuse")

    def join_resp_protocol(self, ip, message):
        self.add_node(ip)
        try:
            ip_list = message.split("|")[1].split(",")
            for ip_node in ip_list:
                if ip_node:
                    self.add_node(ip_node)
        except IndexError:
            pass
        for ip_node in self.other_nodes:
            if ip_node != ip:
                mess = "****joined|" + get_local_ip()
                send_message(ip_node, mess)

    def join_protocol(self, ip, message):
        print("===== Add node")
        self.add_node(ip)
        mess = "****join_resp|"
        for ip_node in self.other_nodes:
            if ip_node != ip:
                mess += ip_node + ","
        mess = mess[:-1]
        send_message(ip, mess)
        mess2 = "****blockchain|"
        last_height = message.split("|")[1]
        list_blocks = []
        for i in range(int(last_height), self.blockchain.get_height() + 1):
            block = self.blockchain.get_block_at_index(i)
            list_blocks.append(block)
        mess2 += json.dumps(list_blocks, cls=BlockEncoder)
        if mess2 != "":
            send_message(ip, mess2)

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
