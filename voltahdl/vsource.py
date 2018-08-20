from .component import TwoPinComponent
from . import units


class VPulse(TwoPinComponent):
    def __init__(self, initial, pulse, delay=0, rise=None, fall=None,
                 width=None):
        super().__init__()

        self.initial = units.check(initial, units.volt)
        self.pulse = units.check(pulse, units.volt)
        self.delay = units.check(delay, units.seconds)
        if rise is not None:
            self.rise = units.check(rise, units.seconds)
        else:
            self.rise = None
        if fall is not None:
            if self.rise is None:
                raise RuntimeError(
                    'If fall time is specified, rise time must be'
                    ' specified'
                )
            self.fall = units.check(fall, units.seconds)
        else:
            self.fall = None
        if width is not None:
            if self.rise is None or self.fall is None:
                raise RuntimeError(
                    'If pulse width is specified, rise time and fall time '
                    'must all be specified'
                )
            self.width = units.check(width, units.seconds)
        else:
            self.width = None

    def spice(self, context):
        return "V{} {} {} PULSE({} {} {} {} {} {})".format(
            context.index('V'),
            context.net(self.pins.a),
            context.net(self.pins.b),
            self.initial.to(units.volt).magnitude,
            self.pulse.to(units.volt).magnitude,
            self.delay.to(units.seconds).magnitude,
            (self.rise.to(units.seconds).magnitude
                if self.rise is not None else ''),
            (self.fall.to(units.seconds).magnitude
                if self.fall is not None else ''),
            (self.width.to(units.seconds).magnitude
                if self.width is not None else ''),
        )
