import os.path
import re

from voltahdl import Component

from ...bus.ddr3 import Ddr3Config, Ddr3Master
from . import pinout


ZYNQ7000_OVERVIEW_DATASHEET_URL =\
    ("https://www.xilinx.com/support/documentation/data_sheets/ds190-Zynq-7000"
     "-Overview.pdf")


class Zynq7000(Component):
    def __init__(self):
        super().__init__()

    def _init_pinout(self, pinout_dir, device, package):
        pinout_file_name = device.lower() + package.lower() + 'pkg.txt'
        pinout_path = os.path.join(pinout_dir, pinout_file_name)
        if not os.path.isfile(pinout_path):
            raise ValueError(
                'Package variant {} is not available for component {}'.format(
                    package, self.__class__.__name__))
        self.package = package.upper()
        self.pinout = pinout.load_pinout(pinout_path)
        pinout.pinout_to_pins(self, self.pinout)


def generate_zynq7000_component(device):
    def __init__(self, package):
        Zynq7000.__init__(self)
        self._init_pinout(os.path.dirname(__file__), device, package)

        # figure out DDR3 addr width, data width, and number of DM pins
        ddr3_data_width = len(
            [p for p in self.pins._get()
             if re.search("PS_DDR_DQ[0-9+]", p.name)]
        )
        ddr3_addr_width = len(
            [p for p in self.pins._get()
             if re.search("PS_DDR_A[0-9+]", p.name)]
        )
        ddr3_num_dm = len(
            [p for p in self.pins._get()
             if re.search("PS_DDR_DM[0-9+]", p.name)]
        )

        ddr3_num_dqs = len(
            [p for p in self.pins._get()
             if re.search("PS_DDR_DQS_P[0-9+]", p.name)]
        )

        self.ddr3_config = Ddr3Config(
            ddr3_addr_width, ddr3_data_width,
            num_cke=1, num_cs=1, num_dm=ddr3_num_dm, num_odt=1,
            num_dqs=ddr3_num_dqs
        )

        self.ddr3_master = Ddr3Master(self.ddr3_config)
        self.ddr3_master.connect_pins_by_pattern(self, '^PS_DDR')

    comp_class = type(device, (Zynq7000,), {'__init__': __init__})
    comp_class.datasheet = ZYNQ7000_OVERVIEW_DATASHEET_URL
    return comp_class


XC7Z007S = generate_zynq7000_component('XC7Z007S')
XC7Z012S = generate_zynq7000_component('XC7Z012S')
XC7Z014S = generate_zynq7000_component('XC7Z014S')
XC7Z010 = generate_zynq7000_component('XC7Z010')
XC7Z015 = generate_zynq7000_component('XC7Z015')
XC7Z020 = generate_zynq7000_component('XC7Z020')
XC7Z030 = generate_zynq7000_component('XC7Z030')
XC7Z035 = generate_zynq7000_component('XC7Z035')
XC7Z045 = generate_zynq7000_component('XC7Z045')
XC7Z100 = generate_zynq7000_component('XC7Z100')
