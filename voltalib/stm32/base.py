from voltahdl import Component

from . import pinout


class STM32Component(Component):
    def __init__(self):
        super().__init__()

    def _init_pinout(self, pinout_path, package):
        packages, self._pinout = pinout.load_pinout(pinout_path)
        if package not in packages:
            raise ValueError(
                'Package variant {} is not available for component {}'.format(
                    package, self.__class__.__name__))
        self.package = package
        pinout.pinout_to_pins(self, self._pinout, package)


def generate_stm32_component(name, base, pinout_path, datasheet_url):
    def __init__(self, package):
        base.__init__(self)
        self._init_pinout(pinout_path, package)

    comp_class = type(name, (base,), {'__init__': __init__})
    comp_class.datasheet = datasheet_url
    return comp_class
