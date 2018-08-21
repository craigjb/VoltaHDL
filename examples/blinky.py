from voltahdl import *
from voltalib.tlc555 import symmetric_oscillator

c = symmetric_oscillator('1 Hz', '10 uF')

c.ports.vcc > c.add('vs', VPulse('0 V', '5 V')) < c.ports.gnd
result = ngspice.transient(c, '100 us', '5 s')

plot.plot(result.time, result.ports.output.v)
plot.show()
