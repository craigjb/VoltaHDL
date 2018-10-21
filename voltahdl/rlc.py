from . import units
from . import def_two_pin_component

Resistor = def_two_pin_component(
    'Resistor', 'R',
    ('a', 'b'),
    required_parameters=[('value', units.ohm)]
)

Inductor = def_two_pin_component(
    'Inductor', 'L',
    ('a', 'b'),
    required_parameters=[('value', units.henry)]
)

Capacitor = def_two_pin_component(
    'Capacitor', 'C',
    ('a', 'b'),
    required_parameters=[('value', units.farad)]
)
