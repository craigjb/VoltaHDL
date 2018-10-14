import inspect

from . import rail


CIRCUIT_STACK = []


def top_circuit():
    return CIRCUIT_STACK[0]


def current_circuit():
    if len(CIRCUIT_STACK) > 0:
        return CIRCUIT_STACK[-1]
    else:
        return None


def collect_components(circuit):
    components = circuit.components.copy()
    for sub_circuit in circuit.sub_circuits:
        components |= collect_components(sub_circuit)
    return components


class Node(object):
    def __init__(self):
        self.net = Net({self})

    def __add__(self, other):
        if isinstance(other, Node):
            return self.connect_node(other)
        elif isinstance(other, Net):
            return self.connect_net(other)
        else:
            raise NotImplementedError

    def __gt__(self, other):
        if isinstance(other, TwoPinComponent):
            self.connect_node(other.pins.a)
            return other
        elif isinstance(other, rail.Rail):
            self.connect_net(other.p)
            return other
        else:
            raise NotImplementedError

    def connect_node(self, other):
        assert self.net is not None
        assert other.net is not None
        # combine the two nets into one
        self.net.nodes |= other.net.nodes
        other.net.nodes = set()
        for node in self.net.nodes:
            node.net = self.net
        return self.net

    def connect_net(self, net):
        net.nodes |= self.net.nodes
        self.net.nodes = set()
        for node in net.nodes:
            node.net = net
        return net


class Net(object):
    def __init__(self, nodes=None):
        self.nodes = nodes or set()

    def __add__(self, other):
        if isinstance(other, Node):
            return other.connect_net(self)
        elif isinstance(other, Net):
            return self.nodes[0].connect_net(other)
        else:
            raise NotImplementedError

    def __gt__(self, other):
        if isinstance(other, TwoPinComponent):
            other.pins.a.connect_net(self)
            return other
        elif isinstance(other, rail.Rail):
            self.nodes[0] + other.p
            return other
        else:
            raise NotImplementedError


GND = Net()


def net_for(n):
    if isinstance(n, Node):
        return n.net
    elif isinstance(n, Net):
        return n
    else:
        raise ValueError('Must be a Node or Net')


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


class CircuitStackPlaceholder(object):
    """
    Used to hold the place and collect components for a Circuit while __init__
    is called. After a new Circuit's __init__ method is finished, the
    placeholder is removed and all the components are put in the new Circuit
    instance.
    """
    def __init__(self):
        self.components = set()


class CircuitMeta(type):
    def __call__(cls, *args, **kwds):
        # push a placeholder onto the stack to contain all of the components
        # created during the new instance's __init__ method
        CIRCUIT_STACK.append(CircuitStackPlaceholder())

        # create new instance and call __init__
        instance = type.__call__(cls, *args, **kwds)

        # pop the instance off the Circuit stack since it's __init__ method is
        # now over and  move components from the placeholder into the created
        # instance
        placeholder = CIRCUIT_STACK.pop()
        instance.components = placeholder.components

        # add the new circuit as a subcircuit to the parent
        current_circuit().sub_circuits.add(instance)

        return instance


class Circuit(object):
    def __init__(self):
        self.components = set()
        self.sub_circuits = set()
        self.ports = Ports(self)
        self.gnd = GND

    def __setattr__(self, name, value):
        """
        Whenever a Component is created and assigned to an instance attribute,
        set the Component's name to that attributes' name. This allows easy
        naming of Components without repetition.
        """
        if isinstance(value, Component):
            value.name = name
            value.circuit = self
        super().__setattr__(name, value)

    def __getattribute__(self, name):
        """
        Whenever a method of the Circuit is called, wrap the method so that the
        Circuit will contain all components created in the method call.
        """
        attr = super().__getattribute__(name)
        if inspect.ismethod(attr):
            def wrap(*args, **kwargs):
                CIRCUIT_STACK.append(self)
                attr(*args, **kwargs)
                CIRCUIT_STACK.pop(self)
            return wrap
        else:
            return attr


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
        port = Port()
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
        if current_circuit() is None:
            raise HierarchyException(
                'A component must be created in a Circuit.')
        current_circuit().components.add(self)
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


class HierarchyException(Exception):
    pass


TOP = Circuit()
CIRCUIT_STACK.append(TOP)
