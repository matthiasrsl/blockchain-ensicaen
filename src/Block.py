from hashlib import sha256


class Block:

    def __init__(self, index, data, previous_hash, date):
        self.previous_hash = previous_hash
        self.index = index
        self.data = data
        self.date = date
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return sha256(f'{self.index}{self.date}{self.data}{self.previous_hash}'.encode('utf-8')).hexdigest()

    def is_previous(self, other):  # declare type block ?
        if not other.previous_hash == self.hash:
            return False
        return True


