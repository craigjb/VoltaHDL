from . import component


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
        if isinstance(other, component.TwoPinComponent):
            self.connect_node(other.pins.a)
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

    def connect_two_pin(self, other):
        return self + other.pins.a

    def connect_net(self, net):
        net.nodes |= self.net.nodes
        self.net.nodes = set()
        for node in net.nodes:
            node.net = net
        return net


class Net(object):
    def __init__(self, nodes=set()):
        self.nodes = nodes

    def __add__(self, other):
        if isinstance(other, Node):
            return other.connect_net(self)
        else:
            raise NotImplementedError

    def __gt__(self, other):
        if isinstance(other, component.TwoPinComponent):
            other.pins.a.connect_net(self)
            return other
        else:
            raise NotImplementedError
