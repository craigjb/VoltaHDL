from . import units
from . import def_two_pin_component

Resistor = def_two_pin_component(
    'Resistor',
    ('a', 'b'),
    required_parameters=[('value', units.ohm)]
)

Inductor = def_two_pin_component(
    'Inductor',
    ('a', 'b'),
    required_parameters=[('value', units.henry)]
)

Capacitor = def_two_pin_component(
    'Capacitor',
    ('a', 'b'),
    required_parameters=[('value', units.farad)]
)
