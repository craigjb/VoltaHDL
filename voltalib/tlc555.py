from voltahdl import *

TLC555 = def_component(
    'TLC555',
    datasheet='http://www.ti.com/lit/ds/symlink/tlc555.pdf'
)


@TLC555.def_pins
def tlc555_pins(pins):
    pins.vcc = Pin(8)
    pins.gnd = Pin(1)
    pins.trigger = Pin(2)
    pins.output = Pin(3)
    pins.reset = Pin(4)
    pins.control = Pin(5)
    pins.threshold = Pin(6)
    pins.discharge = Pin(7)


@TLC555.def_block
def symmetric_oscillator(
        frequency, cap, vdd_decoupling='0.01 uF', resetable=False,
        control_decoupling=None):
    frequency = units.check(frequency, units.hertz)
    cap = units.check(cap, units.farads)
    if control_decoupling is not None:
        control_decoupling = units.check(control_decoupling, units.farads)

    c = Block()
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
    return c
