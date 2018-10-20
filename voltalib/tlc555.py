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
        b, frequency, cap, vdd_decoupling='0.01 uF', resetable=False,
        control_decoupling=None):
    frequency = units.check(frequency, units.hertz)
    cap = units.check(cap, units.farads)
    if control_decoupling is not None:
        control_decoupling = units.check(control_decoupling, units.farads)

    b.tlc555 = TLC555()

    r1_val = 1.0 / (1.443 * (cap.to(units.F).magnitude) *
                    (frequency.to(units.Hz).magnitude))
    b.r1 = R(r1_val * units.ohms)
    b.c1 = C(cap)

    b.tlc555.pins.output > b.r1 < (b.tlc555.pins.threshold +
                                   b.tlc555.pins.trigger)
    b.tlc555.pins.trigger > b.c1 < b.tlc555.pins.gnd

    if not resetable:
        b.tlc555.pins.reset + b.tlc555.pins.vcc

    b.vdd_decoupling = C(vdd_decoupling)
    b.tlc555.pins.vcc > b.vdd_decoupling < b.tlc555.pins.gnd
    if control_decoupling is not None:
        b.control_decoupling = C(control_decoupling)
        b.tlc555.pins.control > b.control_decoupling < b.tlc555.pins.gnd

    b.ports.vcc = b.tlc555.pins.vcc.to_port()
    b.ports.gnd = b.tlc555.pins.gnd.to_port()
    b.ports.output = b.tlc555.pins.output.to_port()

    if resetable:
        b.ports.reset = b.tlc555.pins.reset.to_port()
