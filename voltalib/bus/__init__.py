from voltahdl import Net


class BusNets(object):
    pass


class Bus(object):
    def __init__(self, config):
        self.config = config
        self.nets = BusNets()

    def __plus__(self, other):
        if isinstance(other, Bus):
            if self.config == other.config:
                self._connect_buses(self, other)
            else:
                raise ValueError(
                    'A Bus can only be connected to a bus with the same '
                    'config')
        else:
            raise ValueError('A Bus can only be connected to annother Bus')

    def _connect_buses(self, other):
        for attr in self.nets.__dict__:
            net1 = getattr(self.nets, attr)
            net2 = getattr(other.nets, attr)
            if isinstance(net1, Net):
                net1 + net2


class BusMaster(object):
    def __init__(self, bus):
        self.config = bus.config
        self.bus = bus

    def __plus__(self, other):
        if isinstance(other, Bus):
            other + self.bus
        elif isinstance(other, BusSlave):
            self.bus + other.bus
        else:
            raise ValueError('BusMasters can only be connected to Buses or '
                             'BusSlaves.')


class BusSlave(object):
    def __init__(self, bus):
        self.config = bus.config
        self.bus = bus

    def __plus__(self, other):
        if isinstance(other, Bus):
            other + self.bus
        elif isinstance(other, BusMaster):
            self.bus + other.bus
        else:
            raise ValueError('BusSlaves can only be connected to Buses or '
                             'BusMasters.')

