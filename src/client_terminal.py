import json
from datetime import datetime

from src.block import Block, BlockEncoder
from src.network import send_message


class Client_terminal:
    def __init__(self, handler):
        self.handler = handler
        self.blockchain = handler.blockchain
        while True:
            command = input("command:")
            if command == "create" or command == "c":
                data = input("data:")
                self.create_block(data)

    def send_message(self, message=None):
        if message:
            print(message)
            send_message(self.ip, message)
        else:
            message = "****"
            message += self.lineMessage.toPlainText()
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
