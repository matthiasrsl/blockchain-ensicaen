import json
from datetime import datetime

from src.block import Block, BlockEncoder
from src.network import send_message


class Client_terminal:
    def __init__(self, handler):
        self.handler = handler
        self.blockchain = handler.blockchain

        self.hiddenRefreshButton = type('', (object,), {'click': lambda: self.set_displayer_text})

        bool = input("Are you first? [y/n]:")
        if bool == "n":
            self.blockchain.blocks.clearDB()
        elif bool != "y":
            print("error answer was not n or y")
            exit()

        while True:
            command = input("command:")
            if command == "create" or command == "c":
                data = input("data:")
                self.create_block(data)

            elif command == "me" or command == "message":
                data = input("message:")
                self.send_message(data)

            elif command == "me_ip" or command == "message_to_ip":
                ip = input("ip:")
                data = input("message:")
                self.send_message_to_ip(data, ip)

            elif command == "ma" or command == "manual":
                self.check_receive()

            elif command == "exit":
                exit()

            elif command == "h" or command == "help":
                print("You can use:\n"
                      "- create or c to create a block\n"
                      "- me or message to send a message to all\n"
                      "- me_ip or message_to_ip to send a message to a specific ip\n"
                      "- ma or manual to toggle manual mode\n"
                      "- exit to quit")

            else:
                print("command not recognised, use h or help.")

    def send_message(self, data):
        message = "****"
        message += data
        self.handler.send_message_to_all(message)

    def create_block(self, data):
        last_block = self.blockchain.get_last_block()
        block = Block(last_block.index + 1, data, last_block.hash, datetime.now())
        block.mine()
        message = "****"
        message += "mined_block|"
        message += json.dumps(block, cls=BlockEncoder)
        self.blockchain.add_block(block)
        self.handler.send_message_to_all(message)

    def send_message_to_ip(self, mes, ip):
        message = "****"
        message += mes
        send_message(ip, message)

    def check_receive(self):
        self.handler.manual_validation = self.handler.manual_validation == False  # toggle
        print(f'Manual is enabled:{self.handler.manual_validation}')

    def set_displayer_text(self):
        print(str(self.handler.block_to_add))
