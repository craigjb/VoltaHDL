import os.path
from voltahdl import Component, Pin, Circuit


class TLC555(Component):
    datasheet = "http://www.ti.com/lit/ds/symlink/tlc555.pdf"
    spice_models = {
        'ngspice': os.path.join(os.path.dirname(__file__), 'tlc555.ngspice'),
    }

    def __init__(self):
        super().__init__()

        self.pins.vcc = Pin()
        self.pins.gnd = Pin()
        self.pins.trigger = Pin()
        self.pins.output = Pin()
        self.pins.reset = Pin()
        self.pins.control = Pin()
        self.pins.threshold = Pin()
        self.pins.discharge = Pin()

    def spice(self, context):
        return "X{} {} {} {} {} {} {} {} {} TLC555".format(
            context.index('X'),
            context.net(self.pins.threshold),
            context.net(self.pins.control),
            context.net(self.pins.trigger),
            context.net(self.pins.reset),
            context.net(self.pins.output),
            context.net(self.pins.discharge),
            context.net(self.pins.vcc),
            context.net(self.pins.gnd)
        )
