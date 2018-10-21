from . import units
from .connectivity import Pin
from . import blocks
from . import scoping


class Pins(object):
    """
    Represents a Component's pins.

    Each pin is an attribute on this object, and can be accessed just like
    Python attributes.

    For example: `u1.pins.gnd`

    Adding pins is straightforward as well: `u1.pins.vcc = Pin(12)`
    """

    def __init__(self, component):
        self._pins = {}
        self._pins_by_number = {}
        self._component = component

    def __setattr__(self, name, value):
        # This overrides the Python magic method to set Pin names when they are
        # assigned to a Pins object. This gets of rid of needless verbosity to
        # assign names to Pins and then assign to a binding in the Pins object.
        # i.e. instead of: `u1.pins.gnd = Pin('gnd', 12)`
        # we can do: `u1.pins.gnd = Pin(12)`, and u1.pins.gnd.name is
        # automatically set to 'gnd'
        if isinstance(value, Pin):
            value.name = name
            value.component = self._component
            self._pins[name] = value
            if value.number in self._pins_by_number:
                raise ValueError(
                    'Pin number {} cannot be assigned to multiple pins on '
                    'component {}: {} and {}'.format(
                        value.number, self._component.__class__.__name__,
                        self._pins_by_number[value.number].name, name))
            self._pins_by_number[value.number] = value
        super().__setattr__(name, value)

    def _get(self):
        return self._pins.values()

    def _number(self, num):
        return self._pins_by_number.get(num, None)

    def _add_pin_alias(self, name, pin):
        super().__setattr__(name, pin)

    def _add_pin_number(self, pin, num):
        self._pins_by_number[num] = pin


class Pinout(object):
    def __init__(self, packages):
        self.packages = packages

    def apply(self, c, package):
        if package not in self.packages:
            raise ValueError(
                'Package variant {} is not available for component {}'.format(
                    package, c.__class__.__name__))
        c.package = package


class ComponentBase(object):
    _pin_func = None

    @classmethod
    def def_pins(cls, f):
        """
        Decorator used to specify pins for a Component if not using a Pinout.

        Example:

            Part123 = def_component('Part123')

            @Part123.def_pins
            def part123_pins(pins):
                pins.vcc = Pin(1)
                pins.gnd = Pin(2)
                pins.output = Pin(3)

        """
        cls._pin_func = f
        return f

    @classmethod
    def def_helper(cls, f):
        def helper(self):
            self._helpers.append(f)
        helper.__name__ = f.__name__
        setattr(cls, f.__name__, helper)
        return f

    @classmethod
    def def_block(cls, f):
        def wrapper(*args, **kwargs):
            b = blocks.Block()
            scoping.push_block(b)
            f(b, *args, **kwargs)
            scoping.pop_block()
            return b
        setattr(cls, f.__name__, wrapper)
        return wrapper


class ComponentSeries(ComponentBase):
    pass


class Component(ComponentBase):
    def __init__(self, *args, package=None):
        self._helpers = []
        self.pins = Pins(self)

        if self._pin_func is not None:
            self.__class__._pin_func(self.pins)
        if self.pinout is not None:
            if len(self.pinout.packages) > 1:
                if package is None:
                    raise ValueError(
                        "The component {} has multiple packages available, and"
                        " one must be specified"
                        .format(self.__class__.__name__))
                else:
                    self.pinout.apply(self, package)
            else:
                self.pinout.apply(self, self.pinout.packages[0])

        for i, param in enumerate(self._required_parameters):
            if isinstance(param[1], units.Quantity):
                setattr(self, param[0], units.check(args[i], param[1]))
            else:
                raise ValueError('Unknown parameter type: {}', param[1])

        scoping.current_block().components.add(self)

    def _late_phase(self):
        for func in self._helpers:
            func(self)


class TwoPinComponent(Component):
    def __lt__(self, other):
        return self.pins._second + other


def def_component_series(name, datasheet=None):
    series_class = type(name, (ComponentSeries,), {})
    series_class.datasheet = datasheet
    return series_class


def def_component(name, series=None, datasheet=None, pinout=None,
                  required_parameters=[], base_class=None):
    if not name.isidentifier():
        raise ValueError("Component's name must be a valid Python identifier")

    def __init__(self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)

    if base_class is None:
        base = Component
    else:
        base = base_class
    if series is None:
        comp_class = type(name, (base,), {'__init__': __init__})
    else:
        comp_class = type(name, (base, series,), {'__init__': __init__})
    comp_class.datasheet = datasheet
    comp_class.pinout = pinout
    comp_class._required_parameters = required_parameters
    return comp_class


def def_two_pin_component(name, pin_names, *args, **kwargs):
    if len(pin_names) != 2:
        raise ValueError('A TwoPinComponent can only have two pin names')
    if 'pinout' in kwargs:
        raise ValueError('A TwoPinComponent cannot have a Pinout')

    comp_class = def_component(
        name, *args, pinout=None, base_class=TwoPinComponent, **kwargs
    )

    @comp_class.def_pins
    def two_pins(pins):
        first = Pin(1)
        setattr(pins, pin_names[0], first)
        pins._add_pin_alias('_first', first)
        second = Pin(2)
        setattr(pins, pin_names[1], second)
        pins._add_pin_alias('_second', second)

    return comp_class
