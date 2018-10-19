from voltahdl import *
from voltalib.tlc555 import TLC555


osc = TLC555.symmetric_oscillator('1 Hz', '10 uF')
osc.ports.output > R('1 kohm') < (osc.ports.gnd)
