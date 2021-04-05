import json
import signal
from datetime import datetime

from src.block import Block, BlockEncoder
from src.network import send_message, NetworkHandler


class Client_terminal:
    def __init__(self, handler: NetworkHandler):
        self.handler = handler

        handler.client = self
        self.block_to_accept = False
        signal.signal(signal.SIGINT, self.signal_handler)

        name = input("What's your name?")
        if name == "":
            self.handler.name = "DefaultName"
        else:
            self.handler.name = name

        self.hiddenRefreshButton = type('', (object,), {'click': lambda: self.set_displayer_text()})

        bool = input("Are you first? [y/n]:")
        if bool == "n":
            self.handler.create_blockchain(False)
        elif bool == "y":
            self.handler.create_blockchain(True)
        else:
            print("error answer was not n or y")
            exit()

        print("different print can overlap in this window, don't hesitate to type h to see if you have the hand")

        self.main_command()

    def main_command(self):
        while True:
            command = input("command:")
            if self.handler.manual_validation and self.block_to_accept:
                if command == 'y':
                    self.handler.accept_mined_block()
                    self.block_to_accept = False

                elif command == 'n':
                    self.handler.refuse_mined_block()
                    self.block_to_accept = False

                else:
                    print("error answer was not n or y")

            else:
                if command == "create" or command == "c":
                    data = input("data:")
                    self.create_block(data)

                elif command == "me" or command == "message_to_all":
                    data = input("message:")
                    self.send_message(data)

                elif command == "me_ip" or command == "message_to_ip":

                    ip = input("ip:")

                    data = input("message:")
                    self.send_message_to_ip(data, ip)

                elif command == "ma" or command == "manual":
                    self.check_receive()

                elif command == "exit":
                    self.handler.send_message_to_all("****leave")
                    message_dict = {"sender": "Me", "content": "****leave"}
                    self.handler.message_list.append(message_dict)
                    exit()

                elif command == "h" or command == "help":
                    print("You can use:\n"
                          "- create or c to create a block\n"
                          "- me or message to send a message to all\n"
                          "- me_ip or message_to_ip to send a message to a specific ip\n"
                          "- ma or manual to toggle manual mode\n"
                          "- exit to quit")

                elif command == "r":
                    pass

                else:
                    print("command not recognised, use h or help.")

    def send_message(self, data):
        message = "****"
        message += data
        self.handler.send_message_to_all(message)

    def create_block(self, data):
        last_block = self.handler.blockchain.get_last_blocks()
        block = Block(last_block[0].index + 1, data, last_block[0].hash, datetime.now(), str(self.handler.server_host))
        block.mine(number_0=self.handler.blockchain.number_0)
        message = "****"
        message += "mined_block|"
        message += json.dumps(block, cls=BlockEncoder)
        self.handler.blockchain.new_block(block)
        self.handler.send_message_to_all(message)
        message_dict = {"sender": "Me", "content": message}
        self.handler.message_list.append(message_dict)

    def send_message_to_ip(self, mes, ip):
        message = "****"
        message += mes
        send_message(ip, message)

    def check_receive(self):
        self.handler.manual_validation = self.handler.manual_validation == False  # toggle
        print(f'Manual is enabled:{self.handler.manual_validation}')

    def set_displayer_text(self):
        if self.handler.manual_validation and self.handler.block_to_add:
            print(str(self.handler.block_to_add))
            print("Accept this block? [y/n]")
            self.block_to_accept = True

    def signal_handler(self, sig, frame):
        self.handler.send_message_to_all("****leave")
        message_dict = {"sender": "Me", "content": "****leave"}
        self.handler.message_list.append(message_dict)
        exit()
