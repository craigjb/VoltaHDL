import numpy as np
import pandas

from voltahdl import Pin


REQUIRED_HEADERS = [
    'pin name', 'pin type', 'alternate functions', 'additional functions'
]


def load_pinout(path):
    """
    Parses CSV pin-out files created by copy-and-pasting from STM32 PDF
    datasheet pin tables into Excel and then saving as CSV.

    Returns a tuple with a list of the package variants and a Pandas Dataframe
    with the pin data.

    The Pandas Dataframe has a column for each package variant with the
    pin numbers, plus at least these additional columns:
    'pin name', 'pin type', 'alternate functions', 'additional functions'

    This function handles a lot of clean up, so we don't have to worry about
    things like blank space, weird splitting of cells over multiple lines,
    etc. Pasting from PDFs into Excel is weird...
    """
    data = pandas.read_csv(path)

    # clean out rows with all NaN (blank rows)
    data.dropna(how='all', inplace=True)

    # strip whitespace around column names
    data.rename(
        columns=lambda col: col.strip().lower()
        if col.strip().lower() in REQUIRED_HEADERS else col.strip(),
        inplace=True
    )

    # figure out how many package variants are in the file
    # (must be before the required headers)
    col_names = list(data.columns)
    num_pkgs = min([col_names.index(col) for col in REQUIRED_HEADERS])

    # pasting in from the ST datasheets results in some of the additional
    # function cells getting split over two lines
    # so here, we look for lines with all the pin number cells blank and add
    # the contents of the other cells to the previous line's data
    to_remove = []
    prev_idx = None
    for idx in data.index:
        if all(pandas.isna(data.loc[idx][0:num_pkgs])):
            for col in data.columns[num_pkgs:]:
                if not pandas.isna(data.at[idx, col]):
                    data.at[prev_idx, col] = (data.at[prev_idx, col] +
                                              data.at[idx, col])
            to_remove.append(idx)
            prev_idx = None
        else:
            prev_idx = idx
    data = data[np.logical_not(data.index.isin(to_remove))]

    # some of the integer pin numbers are coming through as floats
    # so let's change those over to int-strings (get rid of decimal point)
    # some pin names (like BGAs) are not ints though, so fail gracefully
    for pkg in data.columns[0:num_pkgs]:
        try:
            data[pkg] = data[pkg].astype(int).astype(str)
            continue
        except ValueError:
            pass
        # if pin numbers are strings, try to remove whitespace
        try:
            data[pkg] = data[pkg].str.strip()
        except AttributeError:
            pass

    # strip whitespace on string fields
    for col in data.columns[num_pkgs:]:
        data[col] = data[col].str.strip()

    return list(data.columns[0:num_pkgs]), data


def pinout_to_pins(component, pinout, package):
    """
    Uses a parsed STM32 pin-out to define pins for a Component.

    Typically, this function is called in the __init__ method of an STM32
    Component class:
        pinout.pinout_to_pins(self, pinout, 'LQFP100')
    """
    pinout = pinout[pinout[package] != '-']
    for idx, row in pinout.iterrows():
        name = row['pin name']
        if hasattr(component.pins, name):
            getattr(component.pins, name).add_number(row[package])
        else:
            setattr(component.pins, name, Pin(row[package]))
