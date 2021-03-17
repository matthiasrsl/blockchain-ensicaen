import json
import select
import socket

from src.block import Block, BlockEncoder
from src.blockchain import Blockchain

SERVER_PORT = 16385
RECV_SIZE = 16384
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
    print(f"SENDING to {ip}: {message}")
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((ip, SERVER_PORT))
    message = message.encode()
    connection.send(message)
    connection.close()


class NetworkHandler:
    def __init__(self, first=False):
        self.other_nodes = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_clients = []
        self.blockchain = None
        self.name = None
        self.server_host = get_local_ip()
        self.message_list = []

        # self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.keep_running_server = True

        self.manual_validation = False
        self.block_to_add = None
        self.wait = False
        self.client = None

    def create_blockchain(self, first):
        self.blockchain = Blockchain(first=first)

    def start_server(self):
        self.server.bind((self.server_host, SERVER_PORT))
        self.server.accept(5)

    def add_node(self, ip):
        node = Node(ip)
        self.other_nodes[ip] = node
        self.updateVisualizer()

    def remove_node(self, ip):
        try:
            del self.other_nodes[ip]
        except KeyError:
            print(f"{ip} tried to be removed but not in list")

    def process_message(self, message, ip):
        print(f"\n\nRECEIVED from {ip}: \n{message}\n\n")

        message_dict = {"sender": ip, "content": message}
        self.message_list.append(message_dict)
        self.updateVisualizerMessage()

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
            self.add_node(ip)
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
        leaves = json.loads(message.split("|")[2])
        for block in blockchain:
            self.blockchain.add_block(Block(**block))

        for leaf in leaves:
            self.blockchain.add_fork(leaf["hash"], leaf["id"])

    def mined_block_protocol(self, message):
        block_info_json = json.loads(message.split("|")[1])
        self.block_to_add = Block(**block_info_json)
        self.client.hiddenRefreshButton.click()
        if self.manual_validation:
            self.wait = True
            while self.wait:
                pass

        else:
            message = self.blockchain.new_block(self.block_to_add)
            for ip_node in self.other_nodes:
                send_message(
                    ip_node, message
                )  
            message_dict = {"sender": "Me", "content": message}
            self.message_list.append(message_dict)

        self.block_to_add = None

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
                send_message(ip_node, "****joined")
        message_dict = {"sender": "Me", "content": "****joined"}
        self.message_list.append(message_dict)

    def join_protocol(self, ip, message):
        print("===== Add node")
        self.add_node(ip)
        mess = "****join_resp|"
        for ip_node in self.other_nodes:
            if ip_node != ip:
                mess += ip_node + ","
        mess = mess[:-1]
        send_message(ip, mess)
        message_dict = {"sender": "Me", "content": mess}
        self.message_list.append(message_dict)
        mess2 = "****blockchain|"
        last_height = message.split("|")[1]
        list_blocks = []

        leaves = self.blockchain.get_leaves()

        for leaf in leaves:
            leaf_block = self.blockchain.get_block(leaf["hash"])
            current_block = leaf_block
            for i in range(int(last_height), leaf_block.index + 1):
                if current_block not in list_blocks:
                    list_blocks.append(current_block)
                if current_block.index != 0:
                    current_block = self.blockchain.get_block(
                        current_block.previous_hash
                    )

        mess2 += json.dumps(list_blocks, cls=BlockEncoder)
        mess2 += "|"

        mess2 += json.dumps(leaves)

        if mess2 != "":
            send_message(ip, mess2)
            message_dict2 = {"sender": "Me", "content": mess2}
            self.message_list.append(message_dict)

    def send_message_to_all(self, message):
        self.updateVisualizerMessage()
        for ip in self.other_nodes.keys():
            send_message(ip, message)


    def updateVisualizer(self):
        all_nodes = []
        for ip in self.other_nodes.keys():
            node = {"name": self.name, "ip": ip}  # "Prenom" to change
            all_nodes.append(node)

        nodes = {"nodes": all_nodes}
        nodes_json = json.dumps(nodes)
        with open("etc/visudata/nodes.json", "w") as file:
            file.write(nodes_json)

    def updateVisualizerMessage(self):
        messages = {"messages": self.message_list}
        messages_json = json.dumps(messages)
        with open("etc/visudata/messages.json", "w") as file:
            file.write(messages_json)

    def accept_mined_block(self):
        self.blockchain.add_fork(self.block_to_add.hash, self.block_to_add.index)
        self.blockchain.add_block(self.block_to_add)

        self.send_message_to_all("****accept")

        self.block_to_add = None
        self.wait = False
        self.client.hiddenRefreshButton.click()

    def refuse_mined_block(self):
        self.send_message_to_all("****refuse")

        self.wait = False
        self.block_to_add = None
        self.client.hiddenRefreshButton.click()

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
                pass
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
