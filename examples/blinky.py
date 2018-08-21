from voltahdl import *
from voltalib import TLC555

c = Circuit()

c.U1 = TLC555()
c.R1 = R('69.3 kohm')
c.C1 = C('10 uF')

c.U1.pins.output > c.R1 < c.U1.pins.threshold + c.U1.pins.trigger > c.C1 < c.U1.pins.gnd
c.U1.pins.reset + c.U1.pins.vcc

c.V1 = VPulse('0 V', '5 V')
c.U1.pins.vcc > c.V1 < c.U1.pins.gnd

c.gnd = c.U1.pins.gnd
result = ngspice.transient(c, '100 us', '5 s')

plot.plot(result.time, result.U1.pins.output.v)
plot.show()
