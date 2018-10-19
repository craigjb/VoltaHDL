from voltahdl import *

from .pinout import Zynq7000Pinout


ZYNQ7000 = def_component_series(
    "ZYNQ7000",
    datasheet='https://www.xilinx.com/support/documentation/data_sheets/ds190-'
              'Zynq-7000-Overview.pdf'
)


def _def_zynq7000_component(name):
    return def_component(
        name,
        series=ZYNQ7000,
        pinout=Zynq7000Pinout(name)
    )


XC7Z007S = _def_zynq7000_component('XC7Z007S')
XC7Z012S = _def_zynq7000_component('XC7Z012S')
XC7Z014S = _def_zynq7000_component('XC7Z014S')
XC7Z010 = _def_zynq7000_component('XC7Z010')
XC7Z015 = _def_zynq7000_component('XC7Z015')
XC7Z020 = _def_zynq7000_component('XC7Z020')
XC7Z030 = _def_zynq7000_component('XC7Z030')
XC7Z035 = _def_zynq7000_component('XC7Z035')
XC7Z045 = _def_zynq7000_component('XC7Z045')
XC7Z100 = _def_zynq7000_component('XC7Z100')
