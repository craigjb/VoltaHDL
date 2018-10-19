import os
import os.path
import re
import io
import pandas

from voltahdl import *

PINOUT_DIR = os.path.dirname(__file__)


class Zynq7000Pinout(Pinout):
    def __init__(self, name):
        # each package has its own file, so find all files that match the file
        # name format to get the list of available packages.
        self.name = name.lower()
        pattern = self.name + '([a-z0-9]+)' + 'pkg.txt'
        self.packages = [
            m.group(1) for m in
            [re.match(pattern, fn) for fn in os.listdir(PINOUT_DIR)]
            if m is not None
        ]

    def apply(self, c, package):
        super().apply(c, package)
        file_name = self.name + package.lower() + 'pkg.txt'
        data = load_pinout(os.path.join(PINOUT_DIR, file_name))
        pinout_to_pins(c, data)


def load_pinout(path):
    """
    Parses a Xilinx pinout text file for Zynq-7000 devices and returns a Pandas
    Dataframe with the pin data. The Pandas Dataframe has columns that match
    the Xilinx text file column names.

    The function handles cleaning up the text-file, since Xilinx uses
    white-space delimeters, but the headers also have whitespace :(
    """
    with open(path, 'r') as fp:
        raw_data = fp.read()

    # for some reason, even the blank lines are full of whitespace, so we need
    # to get rid of the whitespace first before replace multiple contiguous
    # whitespace chars with commas
    raw_data = re.sub('^\s*$', '', raw_data, flags=re.MULTILINE)
    # now replace all occurances of more than one whitespace character in a
    # row with commas
    raw_data = re.sub('[^\S\r\n]{2,}', ',', raw_data)

    # finally parse as CSV
    data = pandas.read_csv(
        io.BytesIO(raw_data.encode('utf-8')), skiprows=1, skipfooter=1,
        engine='python'
    )

    return data


def pinout_to_pins(component, pinout):
    for _, row in pinout.iterrows():
        name = row['Pin Name']
        number = row['Pin']
        if hasattr(component.pins, name):
            # handles the case where the component already has this pin
            # name, but we need to add another pin number (e.g. multiple
            # VDD pins
            getattr(component.pins, name).add_number(number)
        elif component.pins._number(number) is not None:
            # handles the case where the component has multiple pin names
            # at a single pin number (e.g. VDD and VDDA shorted internally)
            component.pins._add_pin_alias(name, component.pins._number(number))
        else:
            setattr(component.pins, name, Pin(number))
