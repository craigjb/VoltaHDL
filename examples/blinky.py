from voltahdl import *
from voltalib.tlc555 import symmetric_oscillator

c = symmetric_oscillator('1 Hz', '10 uF')

c.ports.vcc > c.add('vs', VPulse('0 V', '5 V')) < c.ports.gnd
c.ports.output > c.add('rload', R('1 kohm')) < c.ports.gnd
result = ngspice.transient(c, '1 ms', '5 s', '0.5 s')

plot.plot(result.time, result.ports.output.v, label='output (V))')
plot.plot(result.time, result.tlc555.pins.trigger.v, label='trigger (V)')
plot.plot(result.time, result.tlc555.pins.control.v, label='control (V)')
plot.xlabel('time (s)')
plot.legend(loc='upper left', bbox_to_anchor=(1.04, 1))
plot.subplots_adjust(right=0.7)
plot.grid()
plot.show()
