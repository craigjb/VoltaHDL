class Pin(object):
    def __init__(self, number):
        self.name = None
        self.number = number

    def __repr__(self):
        return '<Pin({0}) : {1}>'.format(self.number, self.name)

    def add_number(self, num):
        if isinstance(self.number, list):
            self.number.append(num)
            self.component.pins._add_pin_number(num, self)
        else:
            self.number = [self.number, num]
            self.component.pins._add_pin_number(num, self)


class Pins(object):
    def __init__(self, component):
        self._pins = {}
        self._pins_by_number = {}
        self._component = component

    def __setattr__(self, name, value):
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


class ComponentSeries(object):
    @classmethod
    def def_late(cls, f):
        def late(self):
            self._late_funcs.append(f)
        late.__name__ = f.__name__
        setattr(cls, f.__name__, late)
        return f


class Component(object):
    def __init__(self, package=None):
        self.pins = Pins(self)
        self._late_funcs = []

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

    @classmethod
    def def_late(cls, f):
        def late(self):
            self._late_funcs.append(f)
        late.__name__ = f.__name__
        setattr(cls, f.__name__, late)
        return f

    def _late_phase(self):
        for func in self._late_funcs:
            func(self)


def def_component_series(name):
    series_class = type(name, (ComponentSeries,), {})
    return series_class


def def_component(name, series=None, datasheet=None, pinout=None):
    if not name.isidentifier():
        raise ValueError("Component's name must be a valid Python identifier")

    def __init__(self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)

    if series is None:
        comp_class = type(name, (Component,), {'__init__': __init__})
    else:
        comp_class = type(name, (Component, series,), {'__init__': __init__})
    comp_class.datasheet = datasheet
    comp_class.pinout = pinout
    return comp_class
