from .nets import Node
from .component import Component


class Port(Node):
    def __init__(self):
        super().__init__()


class Ports(object):
    pass


class Circuit(object):
    def __init__(self):
        self.components = {}
        self.ports = Ports()

    def __setattr__(self, name, value):
        if isinstance(value, Component):
            value.name = name
            value.circuit = self
            self.components[name] = value
        super().__setattr__(name, value)
