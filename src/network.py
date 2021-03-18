import json
import select
import socket

from src.block import Block, BlockEncoder
from src.blockchain import Blockchain

SERVER_PORT = 16385
RECV_SIZE = 16384
LISTEN_TIME = 5


class Node:
    def __init__(self, ip_address, name):
        self.ip_address = ip_address
        self.name = name


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
        self.ip = str(get_local_ip())

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
        self.server.listen(5)

    def add_node(self, ip, name):
        node = Node(ip, name)
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
            self.add_node(ip, message.split("|")[1])
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
                send_message(ip_node, message)
            message_dict = {"sender": "Me", "content": message}
            self.message_list.append(message_dict)

        self.block_to_add = None

    def join_resp_protocol(self, ip, message):
        node_dict_str = message.split("|")[1]
        print(node_dict_str)
        node_dict = json.loads(node_dict_str)
        print(node_dict)
        sender_node_dict = json.loads(message.split("|")[2])
        node_dict[sender_node_dict["ip"]] = sender_node_dict
        self.other_nodes = [Node(node_dict["ip"], node_dict["name"]) for node_dict in node_dict]

        for node in self.other_nodes:
            if ip != node.ip:
                send_message(node.ip, "****joined|" + self.name)
        message_dict = {"sender": "Me", "content": "****joined"}
        self.message_list.append(message_dict)

    def join_protocol(self, ip, message):
        print("===== Add node")
        self.add_node(ip, message.split("|")[1])
        mess = "****join_resp|"
        mess += json.dumps(self.other_nodes, cls=NodeEncoder)
        mess += "|"
        mess += json.dumps(Node(self.ip, self.name), cls=NodeEncoder)
        send_message(ip, mess)
        message_dict = {"sender": "Me", "content": mess}
        self.message_list.append(message_dict)
        mess2 = "****blockchain|"
        list_blocks = []

        leaves = self.blockchain.get_leaves()

        for leaf in leaves:
            leaf_block = self.blockchain.get_block(leaf["hash"])
            current_block = leaf_block
            for i in range(0, leaf_block.index + 1):
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
        for node in self.other_nodes.values():
            node_dic = {"name": node.name, "ip": node.ip_address}  # "Prenom" to change
            all_nodes.append(node_dic)

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


class NodeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Node):
            return {
                "ip": obj.ip_address,
                "name": obj.name,
            }
        return json.JSONEncoder.default(self, obj)
