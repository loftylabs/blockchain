import hashlib

from apistar import types, validators


class Block:

    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.create_hash()

    def create_hash(self):
        return self._do_hash(self.index, self.timestamp, self.data, self.previous_hash)
    
    @staticmethod
    def _do_hash(index, timestamp, data, previous_hash):
        sha = hashlib.sha256()
        sha.update(f"{index}{timestamp}{data}{previous_hash}".encode())
        return sha.hexdigest()


class BlockType(types.Type):
    index = validators.Integer()
    timestamp = validators.DateTime()
    data = validators.Any()
    previous_hash = validators.String()
    hash = validators.String()