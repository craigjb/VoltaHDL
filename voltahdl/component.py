from .nets import Node, Net
from . import circuit


class Pin(Node):
    def __init__(self, number):
        super().__init__()
        self.name = None
        self.number = number

    def add_number(self, num):
        if isinstance(self.number, list):
            self.number.append(num)
        else:
            self.number = [self.number, num]

    def to_port(self):
        port = circuit.Port()
        self + port
        return port


class Pins(object):
    def __init__(self, component):
        self.pins = {}
        self.component = component

    def get(self):
        return self.pins.values()

    def __setattr__(self, name, value):
        if isinstance(value, Pin):
            value.name = name
            value.component = self.component
            self.pins[name] = value
        super().__setattr__(name, value)


class Component(object):
    datasheet = None
    spice_models = {}

    def __init__(self):
        self.name = None
        self.pins = Pins(self)


class TwoPinComponent(Component):
    def __init__(self):
        super().__init__()
        self.pins.a = Pin()
        self.pins.b = Pin()

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.pins.b.connect_node(other)
        elif isinstance(other, Net):
            return self.pins.b.connect_net(other)
        else:
            raise NotImplementedError
