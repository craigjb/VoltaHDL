import os.path
from voltahdl import Component, Pin, Circuit, Port, units, R, C


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


def symmetric_oscillator(
        frequency, cap, vdd_decoupling='0.01 uF', resetable=False,
        control_decoupling=None):
    frequency = units.check(frequency, units.hertz)
    cap = units.check(cap, units.farads)
    if control_decoupling is not None:
        control_decoupling = units.check(control_decoupling, units.farads)

    c = Circuit()
    c.tlc555 = TLC555()

    r1_val = 1.0 / (1.443 * (cap.to(units.F).magnitude) *
                    (frequency.to(units.Hz).magnitude))
    c.r1 = R(r1_val * units.ohms)
    c.c1 = C(cap)

    c.tlc555.pins.output > c.r1 < (c.tlc555.pins.threshold +
                                   c.tlc555.pins.trigger)
    c.tlc555.pins.trigger > c.c1 < c.tlc555.pins.gnd

    if not resetable:
        c.tlc555.pins.reset + c.tlc555.pins.vcc

    c.vdd_decoupling = C(vdd_decoupling)
    c.tlc555.pins.vcc > c.vdd_decoupling < c.tlc555.pins.gnd
    if control_decoupling is not None:
        c.control_decoupling = C(control_decoupling)
        c.tlc555.pins.control > c.control_decoupling < c.tlc555.pins.gnd

    c.ports.vcc = c.tlc555.pins.vcc.to_port()
    c.ports.gnd = c.tlc555.pins.gnd.to_port()
    c.ports.output = c.tlc555.pins.output.to_port()

    if resetable:
        c.ports.reset = c.tlc555.pins.reset.to_port()

    c.gnd = c.ports.gnd
    return c
