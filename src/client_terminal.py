import json
from datetime import datetime

from src.block import Block, BlockEncoder
from src.network import send_message


class Client_terminal:
    def __init__(self, handler):
        self.handler = handler
        self.blockchain = handler.blockchain
        bool = input("Are you first? [y/n]")
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

            if command == "m":
                data = input("message")
                self.send_message(data)

            if command == "m_ip":
                ip = input("ip")
                data = input("message")
                self.send_message_to_ip(data, ip)

    def send_message(self, message=None):
        message = "****"
        message += message
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
