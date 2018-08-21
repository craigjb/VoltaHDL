from . import scope
from . import component
from . import sim


def net_for_node(node):
    return scope.current().node_nets.get(node, None)


def add_node_to_net(node, net):
    scope.current().node_nets[node] = net


def nodes_for_net(net):
    return list(
        {k: v for (k, v)
         in scope.current().node_nets.items()
         if v == net}
        .keys()
     )


class Node(object):
    def __init__(self):
        add_node_to_net(self, Net())

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
        self_net = net_for_node(self)
        other_net = net_for_node(other)
        assert self_net is not None
        assert other_net is not None

        # combine the two nets into one
        other_nodes = nodes_for_net(other_net)
        for n in other_nodes:
            add_node_to_net(n, self_net)
        return self_net

    def connect_two_pin(self, other):
        return self + other.pins.a

    def connect_net(self, net):
        add_node_to_net(self, net)
        return net

    def net(self):
        return net_for_node(self)

    def v(self):
        return sim.SIMULATION_RESULT['v'][net_for_node(self)]

    voltage = v


class Net(object):
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

    def nodes(self):
        return nodes_for_net(self)

    def v(self):
        return sim.SIMULATION_RESULT['v'][self]

    voltage = v

