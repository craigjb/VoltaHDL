from .nets import Node
from . import component


class Port(Node):
    def __init__(self):
        super().__init__()


class Ports(object):
    def __init__(self, circuit):
        self.ports = {}
        self.circuit = circuit

    def get(self):
        return self.ports.values()

    def __setattr__(self, name, value):
        if isinstance(value, Port):
            value.name = name
            value.circuit = self.circuit
            self.ports[name] = value
        super().__setattr__(name, value)


class Circuit(object):
    def __init__(self):
        self.components = {}
        self.ports = Ports(self)

    def __setattr__(self, name, value):
        if isinstance(value, component.Component):
            value.name = name
            value.circuit = self
            self.components[name] = value
        super().__setattr__(name, value)

    def add(self, name, component):
        component.name = name
        component.circuit = self
        self.components[name] = component
        return component
