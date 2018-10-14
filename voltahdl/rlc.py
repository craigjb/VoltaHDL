from .circuit import TwoPinComponent
from . import units


class Resistor(TwoPinComponent):
    def __init__(self, value):
        super().__init__()

        self.value = units.check(value, units.ohm)

    def spice(self, context):
        return "R{} {} {} {}".format(
            context.index('R'),
            context.net(self.pins.a),
            context.net(self.pins.b),
            context.format_units(self.value)
        )

    def __repr__(self):
        return 'Resistor({})'.format(str(self.value))


class Capacitor(TwoPinComponent):
    def __init__(self, value):
        super().__init__()

        self.value = units.check(value, units.farad)

    def spice(self, context):
        return "C{} {} {} {}".format(
            context.index('C'),
            context.net(self.pins.a),
            context.net(self.pins.b),
            context.format_units(self.value)
        )

    def __repr__(self):
        return 'Capacitor({})'.format(str(self.value))


class Inductor(TwoPinComponent):
    def __init__(self, value):
        super().__init__()

        self.value = units.check(value, units.henry)

    def spice(self, context):
        return "L{} {} {} {}".format(
            context.index('L'),
            context.net(self.pins.a),
            context.net(self.pins.b),
            context.format_units(self.value)
        )

    def __repr__(self):
        return 'Inductor({})'.format(str(self.value))
