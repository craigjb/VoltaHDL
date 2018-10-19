import pint


ureg = pint.UnitRegistry()
Quantity = ureg.Quantity


def check(value, unit):
    try:
        v = float(value)
        return Quantity(v, unit)
    except ValueError:
        pass
    if isinstance(value, str):
        try:
            v = ureg(value)
            v.to(unit)
            return v
        except pint.errors.DimensionalityError as e:
            raise e
    elif isinstance(value, Quantity):
        try:
            value.to(unit)
            return value
        except pint.errors.DimensionalityError as e:
            raise e
    else:
        v = Quantity(value, unit)
        try:
            v.to(unit)
            return v
        except pint.errors.DimensionalityError as e:
            raise e


seconds = second = sec = s = ureg('second')
fs = ureg('femtosecond')
ps = ureg('picosecond')
ns = ureg('nanosecond')
us = ureg('microsecond')
ms = ureg('millisecond')

hertz = Hz = ureg('hertz')
kilohertz = KHz = ureg('kilohertz')
megahertz = MHz = ureg('megahertz')
gigahertz = GHz = ureg('gigahertz')
terahertz = THz = ureg('terahertz')

V = volts = volt = ureg('volt')
mV = ureg('mV')
uV = ureg('uV')
nV = ureg('nV')
pV = ureg('pV')
fV = ureg('fV')

mohm = ureg('mohm')
ohm = ohms = ureg('ohm')
kohm = ureg('kohm')
ureg.define('k = 1000 * ohm')
Mohm = ureg('Mohm')

F = farad = farads = ureg('farad')
mF = ureg('mF')
uF = ureg('uF')
nF = ureg('nF')
pF = ureg('pF')
fF = ureg('fF')

H = henry = henries = ureg('henry')
mH = ureg('mH')
uH = ureg('uH')
nH = ureg('nH')
pH = ureg('pH')
fH = ureg('fH')

bit = bits = ureg('bit')
