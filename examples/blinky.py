from voltahdl import *
from voltalib.tlc555 import TLC555


osc = TLC555.SymmetricOscillator('1 Hz', '10 uF')

osc.ports.vcc > VPulse('0 V', '5 V') < (osc.ports.gnd + GND)
osc.ports.output > R('1 kohm') < (osc.ports.gnd + GND)

result = ngspice.transient('1 ms', '5 s', '0.5 s')

# plot.plot(result.time, result.ports.output.v, label='output (V))')
# plot.plot(result.time, result.tlc555.pins.trigger.v, label='trigger (V)')
# plot.plot(result.time, result.tlc555.pins.control.v, label='control (V)')
# plot.xlabel('time (s)')
# plot.legend(loc='upper left', bbox_to_anchor=(1.04, 1))
# plot.subplots_adjust(right=0.7)
# plot.grid()
# plot.show()
