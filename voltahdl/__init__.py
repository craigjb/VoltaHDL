from . import units
from .component import Component, Pin
from .circuit import Circuit, Port
from .rail import Rail
from .rlc import Resistor, Capacitor, Inductor
from .vsource import VPulse
from . import ngspice

from matplotlib import pyplot as plot
import numpy as np


R = Resistor
C = Capacitor
L = Inductor
