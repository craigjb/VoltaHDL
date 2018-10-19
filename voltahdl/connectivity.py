from . import component


class Node(object):
    def __init__(self):
        self.net = Net({self})

    def __add__(self, other):
        return self.net.__add__(other)

    def __gt__(self, other):
        return self.net.__gt__(other)


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


class Port(Node):
    def __init__(self):
        super().__init__()
        self.name = None

    def __repr__(self):
        return '<Port : {}>'.format(self.name)


class Net(object):
    def __init__(self, nodes=None):
        self.nodes = nodes or set()

    def __add__(self, other):
        if isinstance(other, Node):
            return self.connect_node(other)
        elif isinstance(other, Net):
            return self.connect_net(other)
        else:
            raise NotImplementedError

    def __gt__(self, other):
        if isinstance(other, component.TwoPinComponent):
            self.connect_node(other.pins._first)
            return other
        else:
            raise NotImplementedError

    def connect_net(self, net):
        net.nodes |= self.nodes
        self.nodes = set()
        for node in net.nodes:
            node.net = net
        return net

    def connect_node(self, other):
        assert other.net is not None
        # combine the two nets into one
        self.nodes |= other.net.nodes
        other.net.nodes = set()
        for node in self.nodes:
            node.net = self
        return self
