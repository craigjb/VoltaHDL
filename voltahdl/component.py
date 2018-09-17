from .nets import Node, Net
from . import circuit


class Pin(Node):
    def __init__(self, number):
        super().__init__()
        self.name = None
        self.number = number

    def __repr__(self):
        return '<Pin({0}) : {1}>'.format(self.number, self.name)

    def add_number(self, num):
        if isinstance(self.number, list):
            self.number.append(num)
            self.component.pins._add_pin_number(num, self)
        else:
            self.number = [self.number, num]
            self.component.pins._add_pin_number(num, self)

    def to_port(self):
        port = circuit.Port()
        self + port
        return port


class Pins(object):
    def __init__(self, component):
        self._pins = {}
        self._pins_by_number = {}
        self._component = component

    def _get(self):
        return self._pins.values()

    def _number(self, num):
        return self._pins_by_number.get(num, None)

    def __setattr__(self, name, value):
        if isinstance(value, Pin):
            value.name = name
            value.component = self._component
            self._pins[name] = value
            if value.number in self._pins_by_number:
                raise ValueError(
                    'Pin number {} cannot be assigned to multiple pins on '
                    'component {}: {} and {}'.format(
                        value.number, self._component.__class__.__name__,
                        self._pins_by_number[value.number].name, name))
            self._pins_by_number[value.number] = value
        super().__setattr__(name, value)

    def _add_pin_alias(self, name, pin):
        super().__setattr__(name, pin)

    def _add_pin_number(self, pin, num):
        self._pins_by_number[num] = pin


class Component(object):
    datasheet = None
    spice_models = {}

    def __init__(self):
        self.name = None
        self.pins = Pins(self)


class TwoPinComponent(Component):
    def __init__(self):
        super().__init__()
        self.pins.a = Pin(1)
        self.pins.b = Pin(2)

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.pins.b.connect_node(other)
        elif isinstance(other, Net):
            return self.pins.b.connect_net(other)
        else:
            raise NotImplementedError
