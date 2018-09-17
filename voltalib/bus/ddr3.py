from voltahdl import units, Net
from voltahdl.utilities import find_pin

from . import Bus, BusMaster, BusSlave


class Ddr3Config(object):
    def __init__(self, addr_width, data_width,
                 num_cke, num_cs, num_dm, num_odt, num_dqs):
        self.addr_width = units.check(addr_width, units.bits)
        self.data_width = units.check(data_width, units.bits)
        self.num_cke = num_cke
        self.num_cs = num_cs
        self.num_dm = num_dm
        self.num_odt = num_odt
        self.num_dqs = num_dqs

    def __eq__(self, other):
        return (
            self.addr_width == other.addr_width and
            self.data_width == other.data_width and
            self.num_cke == other.num_cke and
            self.num_cs == other.num_cs and
            self.num_dm == other.num_dm and
            self.num_odt == other.num_odt and
            self.num_dqs == other.num_dqs
        )


class Ddr3Bus(Bus):
    def __init__(self, config):
        super().__init__(config)

        self.nets.RESET_n = Net()
        self.nets.CK_P, self.nets.CK_N = Net(), Net()
        self._gen_ddr3_nets('CKE{0}', config.num_cke)
        self._gen_ddr3_nets('CS{0}_n', config.num_cs)
        self._gen_ddr3_nets('DM{0}', config.num_dm)
        self._gen_ddr3_nets('ODT{0}', config.num_odt)
        self._gen_ddr3_nets('DQS{0}_P', config.num_dqs)
        self._gen_ddr3_nets('DQS{0}_N', config.num_dqs)
        self.nets.RAS_n = Net()
        self.nets.CAS_n = Net()
        self.nets.WE_n = Net()
        self.nets.BA0 = Net()
        self.nets.BA1 = Net()
        self.nets.BA2 = Net()
        self._gen_ddr3_nets('A{0}', config.addr_width.magnitude)
        self._gen_ddr3_nets('DQ{0}', config.data_width.magnitude)

    def _gen_ddr3_nets(self, fmt, num):
        if num == 1:
            setattr(self.nets, fmt.format(''), Net())
        else:
            nets = []
            for i in range(num):
                n = Net()
                setattr(self.nets, fmt.format(i), n)
                nets.append(n)
            setattr(self.nets, fmt.format(''), nets)


class Ddr3Master(BusMaster):
    def __init__(self, config):
        super().__init__(Ddr3Bus(config))

    def connect_pins_by_pattern(self, component, ddr3_pattern):
        find_pin('RESET|RST', component, ddr3_pattern) + self.bus.nets.RESET_n
        find_pin('CK[_]*P', component, ddr3_pattern) + self.bus.nets.CK_P
        find_pin('CK[_]*N', component, ddr3_pattern) + self.bus.nets.CK_N
        find_pin('RAS', component, ddr3_pattern) + self.bus.nets.RAS_n
        find_pin('CAS', component, ddr3_pattern) + self.bus.nets.CAS_n
        find_pin('WE', component, ddr3_pattern) + self.bus.nets.WE_n
        self._connect_multiple_pins_by_pattern(
            'CKE{0}', 'CKE{0}', self.config.num_cke, component, ddr3_pattern)
        self._connect_multiple_pins_by_pattern(
            'CS{0}', 'CS{0}_n', self.config.num_cs, component, ddr3_pattern)
        self._connect_multiple_pins_by_pattern(
            'DM{0}', 'DM{0}', self.config.num_dm, component, ddr3_pattern)
        self._connect_multiple_pins_by_pattern(
            'ODT{0}', 'ODT{0}', self.config.num_odt, component, ddr3_pattern)
        self._connect_multiple_pins_by_pattern(
            'DQS{0}_P|DQS_P{0}', 'DQS{0}_P', self.config.num_dqs,
            component, ddr3_pattern)
        self._connect_multiple_pins_by_pattern(
            'DQS{0}_N|DQS_N{0}', 'DQS{0}_N', self.config.num_dqs,
            component, ddr3_pattern)
        self._connect_multiple_pins_by_pattern(
            '(^|[^B])A{0}([^0-9]|$)', 'A{0}', self.config.addr_width.magnitude,
            component, ddr3_pattern)
        self._connect_multiple_pins_by_pattern(
            'DQ{0}([^0-9]|$)', 'DQ{0}', self.config.data_width.magnitude,
            component, ddr3_pattern)

    def _connect_multiple_pins_by_pattern(self, pattern_fmt, net_fmt, num,
                                          component, ddr3_pattern):
        if num == 1:
            (find_pin(pattern_fmt.format(''), component,
                      prefilter=ddr3_pattern) +
                getattr(self.bus.nets, net_fmt.format('')))
        else:
            for i in range(num):
                (find_pin(pattern_fmt.format(i), component,
                          prefilter=ddr3_pattern) +
                    getattr(self.bus.nets, net_fmt.format(i)))


class Ddr3Slave(BusSlave):
    def __init__(self, config):
        super().__init__(Ddr3Bus(config))
