from .nets import Node


class Port(Node):
    def __init__(self):
        super().__init__()


class Ports(object):
    pass


class Circuit():
    def __init__(self):
        self.ports = Ports()
