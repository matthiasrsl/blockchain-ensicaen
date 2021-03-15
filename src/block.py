import json
from hashlib import sha256
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
        """
        calculate hash
        :return: the sha256 of a block
        :rtype:Hexadecimal String
        """
        return sha256(
            f"{self.index}${self.nonce}${self.date}${self.data}${self.previous_hash}".encode(
                "utf-8"
            )
        ).hexdigest()

    def mine(self, number_0=2):
        """
        mine a block
        :param number_0:The difficulty
        :type number_0:int
        """
        time_begin = time()
        while self.hash[:number_0] != number_0 * "0":
            self.nonce += 1
            self.hash = self.calculate_hash()
        time_end = time()
        mining_duration = "{:4.3f}".format(time_end - time_begin)
        print(
            f"Block {self.index} mined in {mining_duration}s, nounce is {self.nonce}"
        )

    def is_valid(self, number_0=2):
        """
        Verify that a block is mined and valid
        :param number_0:The difficulty
        :type number_0:int
        :return:
        :rtype: bool
        """
        if self.hash != self.calculate_hash():
            return False
        if self.hash[:number_0] != number_0 * "0":
            return False
        return True

    def is_previous(self, other):  # declare type block ? (faire passer en argument seulement le hash au lieu du block pour reduire le temps d'éxécution)
        """
        check if the other block is previous
        :param other: A block to check
        :type other: Block
        :return: the answer
        :rtype:bool
        """
        return other.previous_hash == self.hash


    def __eq__(self, other):
        return self.hash == other.hash

    def __str__(self):
        return f"{self.index}${self.nonce}${self.date}${self.data}${self.previous_hash}${self.hash}"



class BlockEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Block):
            return {
                "previous_hash": obj.previous_hash,
                "index": obj.index,
                "nonce": obj.nonce,
                "data": obj.data,
                "date": str(obj.date),
                "hash": obj.hash,
            }
        return json.JSONEncoder.default(self, obj)
