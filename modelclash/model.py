import os

class Model:
    def __init__(self, name):
        self.name = name
        self.unique_id = f"{name}_{os.urandom(4).hex()}"

    def new_instance(self):
        return Model(self.name)