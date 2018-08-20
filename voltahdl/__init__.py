from . import units
from .component import Component, Pin
from .circuit import Circuit, Port
from .rlc import Resistor, Capacitor, Inductor
from .vsource import VPulse
from .sim import simulation
from . import ngspice

from matplotlib import pyplot as plot
import numpy as np


R = Resistor
C = Capacitor
L = Inductor
