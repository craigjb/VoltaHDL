from voltahdl import *
from voltalib import TLC555

U1 = TLC555()
R1 = R('69.3 kohm')
C1 = C('10 uF')

U1.pins.output > R1 < U1.pins.threshold + U1.pins.trigger > C1 < U1.pins.gnd
U1.pins.reset + U1.pins.vcc

V1 = VPulse('0 V', '5 V')
U1.pins.vcc > V1 < U1.pins.gnd
ngspice.transient(U1.pins.gnd, '100 us', '5 s')

plot.plot(sim.time(), U1.pins.output.v())
plot.show()
