import os.path
from voltahdl import Component, Pin, Circuit, units, R, C


class TLC555(Component):
    datasheet = "http://www.ti.com/lit/ds/symlink/tlc555.pdf"
    spice_models = {
        'ngspice': os.path.join(os.path.dirname(__file__), 'tlc555.ngspice'),
    }

    def __init__(self):
        super().__init__()

        self.pins.vcc = Pin(8)
        self.pins.gnd = Pin(1)
        self.pins.trigger = Pin(2)
        self.pins.output = Pin(3)
        self.pins.reset = Pin(4)
        self.pins.control = Pin(5)
        self.pins.threshold = Pin(6)
        self.pins.discharge = Pin(7)

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

    class SymmetricOscillator(Circuit):
        def __init__(self, frequency, cap, vdd_decoupling='0.01 uF',
                     resetable=False, control_decoupling=None):
            super().__init__()

            frequency = units.check(frequency, units.hertz)
            cap = units.check(cap, units.farads)
            if control_decoupling is not None:
                control_decoupling = units.check(
                    control_decoupling, units.farads)

            self.tlc555 = TLC555()

            r1_val = 1.0 / (1.443 * (cap.to(units.F).magnitude) *
                            (frequency.to(units.Hz).magnitude))
            self.r1 = R(r1_val * units.ohms)
            self.c1 = C(cap)

            self.tlc555.pins.output > self.r1 < (self.tlc555.pins.threshold +
                                                 self.tlc555.pins.trigger)
            self.tlc555.pins.trigger > self.c1 < self.tlc555.pins.gnd

            if not resetable:
                self.tlc555.pins.reset + self.tlc555.pins.vcc

            self.vdd_decoupling = C(vdd_decoupling)
            self.tlc555.pins.vcc > self.vdd_decoupling < self.tlc555.pins.gnd
            if control_decoupling is not None:
                self.control_decoupling = C(control_decoupling)
                (self.tlc555.pins.control > self.control_decoupling
                 < self.tlc555.pins.gnd)

            self.ports.vcc = self.tlc555.pins.vcc.to_port()
            self.ports.gnd = self.tlc555.pins.gnd.to_port()
            self.ports.output = self.tlc555.pins.output.to_port()

            if resetable:
                self.ports.reset = self.tlc555.pins.reset.to_port()

            self.gnd = self.ports.gnd
