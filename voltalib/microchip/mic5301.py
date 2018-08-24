import os.path

import pandas

from voltahdl import Circuit, Component, Pin, R, C, units


def _load_variants(path):
    data = pandas.read_csv(path)

    # clean out rows with all NaN (blank rows)
    data.dropna(how='all', inplace=True)

    # strip whitespace around column names
    data.rename(
        columns=lambda col: col.strip().lower(),
        inplace=True
    )

    # strip whitespace on package column
    data['package'] = data['package'].str.strip()

    # strip trailing 'V' off of output voltage column and convert to floats
    data['output voltage'] = data['output voltage'].str.strip()
    return data


class MIC5301(Component):
    datasheet = 'http://ww1.microchip.com/downloads/en/DeviceDoc/mic5301.pdf'
    _variants = _load_variants(
        os.path.join(os.path.dirname(__file__), 'MIC5301.csv')
    )

    @classmethod
    def has_variant(cls, package, vout):
        if (isinstance(vout, str) and
                (vout.lower() == 'adj' or vout.lower() == 'adj.')):
            # handle 'ADJ' or 'ADJ.' variants
            vout_str = 'ADJ.'
        else:
            # for fixed voltages, check units
            vout = units.check(vout, units.volts).to(units.volts)
            vout_str = '{:.2}'.format(vout.magnitude) + 'V'

        # check the vout and package combination are in the variant list
        if cls._variants[
                (cls._variants['package'] == package) &
                (cls._variants['output voltage'] == vout_str)].empty:
            return False
        else:
            return True

    def __init__(self, package, vout):
        super().__init__()

        if (isinstance(vout, str) and
                (vout.lower() == 'adj' or vout.lower() == 'adj.')):
            # handle 'ADJ' or 'ADJ.' variants
            self.vout = 'ADJ.'
        else:
            # for fixed voltages, check units
            self.vout = units.check(vout, units.volts).to(units.volts)

        # check the vout and package combination are in the variant list
        if not MIC5301.has_variant(package, vout):
            raise ValueError(
                'The compoent {} does not have a variant with vout = {} '
                'and package {}'.format(
                    self.__class__.__name__, vout, package))
        self.package = package

        if self.package == 'MLF-6':
            self.pins.EN = Pin(1)
            self.pins.GND = Pin(2)
            self.pins.VIN = Pin(3)
            self.pins.OUT = Pin(4)
            if self.vout == 'ADJ.':
                self.pins.ADJ = Pin(5)
            self.pins.BYP = Pin(6)
            self.pins.GND.add_number('PAD')
        elif self.package == 'TSOT-23':
            self.pins.EN = Pin(3)
            self.pins.GND = Pin(2)
            self.pins.VIN = Pin(1)
            self.pins.OUT = Pin(5)
            if self.vout == 'ADJ.':
                self.pins.ADJ = Pin(4)
            else:
                self.pins.BYP = Pin(4)


def mic5301_ldo(package, vout, with_enable=False, adj_r1='10 kohm'):
    vout = units.check(vout, units.volts).to(units.volts)

    c = Circuit()

    if MIC5301.has_variant(package, vout):
        c.mic5301 = MIC5301(package, vout)
    else:
        if not (vout.magnitude >= 1.25 and vout.magnitude <= 5.5):
            raise ValueError('MIC5301 vout must be between 1.25V and 5.5V')
        c.mic5301 = MIC5301(package, 'ADJ.')

        # calculate resistor network
        if vout.magnitude > 1.25:
            vref = 1.25
            adj_r1 = units.check(adj_r1, units.ohms).to(units.ohms)
            adj_r2 = (adj_r1.magnitude * vref) / (vout.magnitude - vref)
            c.r1 = R(adj_r1)
            c.r2 = R(adj_r2)
            c.mic5301.pins.OUT > c.r1 < c.mic5301.pins.ADJ \
                > c.r2 < c.mic5301.pins.GND
        else:
            # for 1.25V out, no resistor network required
            c.mic5301.pins.OUT + c.mic5301.pins.ADJ

    # optional enable input or just tie to VIN for always-on
    c.ports.vin = c.mic5301.pins.VIN.to_port()
    c.ports.vout = c.mic5301.pins.OUT.to_port()
    if with_enable:
        c.ports.enable = c.mic5301.pins.EN.to_port()
    else:
        c.mic5301.pins.EN + c.mic5301.pins.VIN

    # input and output decoupling
    c.cin = C('1 uF')
    c.mic5301.pins.VIN > c.cin < c.mic5301.pins.GND
    c.cout = C('1 uF')
    c.mic5301.pins.OUT > c.cout < c.mic5301.pins.GND

    # bypass VREF is pin is there
    if hasattr(c.mic5301.pins, 'BYP'):
        c.cbyp = C('0.01 uF')
        c.mic5301.pins.BYP > c.cbyp < c.mic5301.pins.GND
    return c
