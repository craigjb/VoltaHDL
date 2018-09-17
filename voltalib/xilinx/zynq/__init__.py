import os.path

from voltahdl import Component

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

    comp_class = type(device, (Zynq7000,), {'__init__': __init__})
    comp_class.datasheet = ZYNQ7000_OVERVIEW_DATASHEET_URL
    return comp_class


XC7Z007S = generate_zynq7000_component("XC7Z007S")
XC7Z012S = generate_zynq7000_component("XC7Z012S")
XC7Z014S = generate_zynq7000_component("XC7Z014S")
XC7Z010 = generate_zynq7000_component("XC7Z010")
XC7Z015 = generate_zynq7000_component("XC7Z015")
XC7Z020 = generate_zynq7000_component("XC7Z020")
XC7Z030 = generate_zynq7000_component("XC7Z030")
XC7Z035 = generate_zynq7000_component("XC7Z035")
XC7Z045 = generate_zynq7000_component("XC7Z045")
XC7Z100 = generate_zynq7000_component("XC7Z100")
