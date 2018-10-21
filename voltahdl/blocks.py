import copy

from .connectivity import Port


class Ports(object):
    """
    Represents a Blocks's ports.

    Each port is an attribute on this object, and can be accessed just like
    Python attributes.

    For example: `block.ports.gnd`

    Adding ports is straightforward as well: `block.ports.vcc = Port()`
    """
    def __init__(self, block):
        self._block = block

    def __setattr__(self, name, value):
        # This works similar to the magic for Pins
        # (more info in the Pins class in component.py)
        if isinstance(value, Port):
            value.name = name
            value.block = self._block
        super().__setattr__(name, value)


class Block(object):
    def __init__(self):
        self.parent = None
        self.children = set()
        self.components = set()
        self.ports = Ports(self)


def flatten_components(b):
    components = copy.copy(b.components)
    for child in b.children:
        components |= flatten_components(child)
    return components
