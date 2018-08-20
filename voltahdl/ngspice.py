import os
import os.path
import tempfile
import subprocess
import io

import numpy as np

from . import scope
from . import nets
from . import units


class NgspiceContext(object):
    def __init__(self):
        self.net_counter = 1
        self.net_mapping = {}
        self.indices = {}

    def index(self, des):
        if des not in self.indices:
            self.indices[des] = 1
        else:
            self.indices[des] += 1
        return self.indices[des]

    def net(self, node):
        net = nets.net_for_node(node)
        if net is None:
            raise RuntimeError(
                'Nodes must have assigned nets for Ngspice simulation')
        if net not in self.net_mapping:
            self.net_mapping[net] = self.net_counter
            self.net_counter += 1
        return self.net_mapping[net]

    def format_units(self, value):
        compatible = value.compatible_units()
        if units.seconds.u in compatible:
            return spice_format_seconds(value)
        elif units.volts.u in compatible:
            return spice_format_volts(value)
        elif units.ohm.u in compatible:
            return spice_format_ohms(value)
        elif units.farad.u in compatible:
            return spice_format_farads(value)
        elif units.henry.u in compatible:
            return spice_format_henries(value)
        else:
            raise RuntimeError('This unit is not implemented for Ngspice yet')


def transient(gnd, tstep, tstop, tstart=0, tmax=None):
    tstep = units.check(tstep, units.seconds)
    tstop = units.check(tstop, units.seconds)
    tstart = units.check(tstart, units.seconds)
    if tmax is not None:
        tmax = units.check(tmax, units.seconds)

    context = NgspiceContext()
    # Ngspice wants gnd as net 0
    if isinstance(gnd, nets.Node):
        context.net_mapping[gnd.net()] = 0
    elif isinstance(gnd, nets.Net):
        context.net_mapping[gnd] = 0
    else:
        raise RuntimeError('gnd must be a net or node')

    spice = 'Volta Transient\n\n'
    components = scope.current().components
    spice += generate_includes(components)
    spice += generate_components(context, components)
    spice += '.tran {} {} {} {}\n\n'.format(
        spice_format_seconds(tstep),
        spice_format_seconds(tstop),
        spice_format_seconds(tstart),
        spice_format_seconds(tmax) if tmax is not None else ''
    )
    spice += generate_control(context)
    spice += '.end'
    raw_output = run(spice)
    parsed = parse_ngspice_binary(raw_output)
    return parsed


def generate_includes(components):
    includes = ''
    for component in components:
        if 'ngspice' in component.spice_models:
            includes += (
                '.include ' +
                os.path.abspath(component.spice_models['ngspice']) +
                '\n'
             )
    return includes + '\n'


def generate_components(context, components):
    spice = ''
    for component in components:
        spice += component.spice(context) + '\n'
    return spice + '\n'


def generate_control(context):
    spice = '.control\n'
    spice += 'save ' + ' '.join([
        'v({})'.format(n)
        for n in context.net_mapping.values()
    ]) + '\n'
    spice += '.endc\n\n'
    return spice


def run(spice):
    input_handle, input_path = tempfile.mkstemp()
    print(input_path)
    os.write(input_handle, spice.encode('utf-8'))
    os.close(input_handle)
    output_handle, output_path = tempfile.mkstemp()
    os.close(output_handle)
    print(output_path)
    subprocess.check_call(['ngspice', '-r', output_path, '-b', input_path])
    with open(output_path, 'rb') as fp:
        raw_output = fp.read()
    try:
        os.remove(input_path)
    except os.error:
        pass
    try:
        os.remove(output_path)
    except os.error:
        pass
    return raw_output


def spice_format_seconds(v):
    if v.units == units.fs:
        return str(v.magnitude) + 'f'
    elif v.units == units.ps:
        return str(v.magnitude) + 'p'
    elif v.units == units.ns:
        return str(v.magnitude) + 'n'
    elif v.units == units.us:
        return str(v.magnitude) + 'u'
    elif v.units == units.ms:
        return str(v.magnitude) + 'm'
    else:
        return str(v.to(units.seconds).magnitude)


def spice_format_volts(v):
    if v.units == units.fV:
        return str(v.magnitude) + 'f'
    elif v.units == units.pV:
        return str(v.magnitude) + 'p'
    elif v.units == units.nV:
        return str(v.magnitude) + 'n'
    elif v.units == units.uV:
        return str(v.magnitude) + 'u'
    elif v.units == units.mV:
        return str(v.magnitude) + 'm'
    else:
        return str(v.to(units.volts).magnitude)


def spice_format_ohms(v):
    if v.units == units.mohm:
        return str(v.magnitude) + 'm'
    elif v.units == units.kohm:
        return str(v.magnitude) + 'k'
    elif v.units == units.Mohm:
        return str(v.magnitude) + 'MEG'
    else:
        return str(v.to(units.ohms).magnitude)


def spice_format_farads(v):
    if v.units == units.fF:
        return str(v.magnitude) + 'f'
    elif v.units == units.pF:
        return str(v.magnitude) + 'p'
    elif v.units == units.nF:
        return str(v.magnitude) + 'n'
    elif v.units == units.uF:
        return str(v.magnitude) + 'u'
    elif v.units == units.mF:
        return str(v.magnitude) + 'm'
    else:
        return str(v.to(units.farads).magnitude)


def spice_format_henries(v):
    if v.units == units.fH:
        return str(v.magnitude) + 'f'
    elif v.units == units.pH:
        return str(v.magnitude) + 'p'
    elif v.units == units.nH:
        return str(v.magnitude) + 'n'
    elif v.units == units.uH:
        return str(v.magnitude) + 'u'
    elif v.units == units.mH:
        return str(v.magnitude) + 'm'
    else:
        return str(v.to(units.henries).magnitude)


def parse_ngspice_binary(raw):
    fp = io.BytesIO(raw)
    flags = []
    var_names = []
    while True:
        line = fp.readline(512).decode('utf-8').strip()
        if line.startswith('Flags:'):
            flags = line.split(' ')[1:]
        elif line.startswith('No. Variables:'):
            num_vars = int(line.split(' ')[-1])
        elif line.startswith('No. Points:'):
            num_points = int(line.split(' ')[-1])
        elif line.startswith('Variables:'):
            for i in range(0, num_vars):
                line = fp.readline(512).decode('utf-8').strip()
                index, name, kind = line.split()
                var_names.append(name)
        elif line.startswith('Binary:'):
            break
    num_format = np.complex if 'complex' in flags else np.float_
    np_dtype = np.dtype({
        'names': var_names,
        'formats': [num_format] * num_vars
    })
    data = np.fromstring(fp.read(), dtype=np_dtype, count=num_points)
    return data
