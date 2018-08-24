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


def generate_stm32_component(name, pinout_path):
    def __init__(self, package):
        STM32Component.__init__(self)

        self._init_pinout(pinout_path, package)

    return type(name, (STM32Component,), {'__init__': __init__})