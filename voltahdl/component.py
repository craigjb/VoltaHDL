from . import scope
from .nets import Node, Net


class Pin(Node):
    def __init__(self):
        super().__init__()


class Pins(object):
    def __init__(self, component):
        self.component = component

    def __setattr__(self, name, value):
        if isinstance(value, Pin):
            value.name = name
            value.component = self.component
        super().__setattr__(name, value)


class Component(object):
    datasheet = None
    spice_models = {}

    def __init__(self):
        self.pins = Pins(self)
        scope.add_component(self)


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
