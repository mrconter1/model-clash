import uuid

class Model:
    def __init__(self, name, provider):
        self.name = name
        self.provider = provider
        self.unique_id = f"{name}_{uuid.uuid4().hex[:8]}"

    def new_instance(self):
        return Model(self.name, self.provider)