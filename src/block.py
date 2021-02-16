from hashlib import sha256
from json import *
from time import time


class Block:
    def __init__(self, index, data, previous_hash, date, nonce=0, **kwargs):
        self.previous_hash = previous_hash
        self.index = index
        self.nonce = nonce
        self.data = data
        self.date = date
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return sha256(
            f"{self.index}${self.nonce}${self.date}${self.data}${self.previous_hash}".encode(
                "utf-8"
            )
        ).hexdigest()

    def mine(self):
        time_begin = time()
        while self.hash[:2] != "00":
            self.nonce += 1
            self.hash = self.calculate_hash()
        time_end = time()
        mining_duration = "{:4.3f}".format(time_end - time_begin)
        print(
            f"Block {self.index} mined in {mining_duration}s, nounce is {self.nonce}"
        )

    def is_valid(self):
        if self.hash != self.calculate_hash():
            return False
        if self.hash[:2] != "00":
            return False
        return True

    def is_previous(self, other):  # declare type block ?
        if not other.previous_hash == self.hash:
            return False
        return True

    def __eq__(self, other):
        return self.hash == other.hash

    def __str__(self):
        return f"{self.index}${self.nonce}${self.date}${self.data}${self.previous_hash}${self.hash}"

    def to_json(self):
        return dumps(self, default=lambda o: o.__dict__)


