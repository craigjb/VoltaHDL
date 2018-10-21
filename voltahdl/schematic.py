import os
import os.path
import tempfile
import subprocess
import json

from . import blocks


def block_to_elk(block):
    """
    Converts a block hierarchy into a ELK input JSON file for layout into a
    schematic.
    """
    components = blocks.flatten_components(block)
    return {
        'id': 'SCHEMATIC',
        'children': [component_to_elk(c) for c in components],
        'properties': {
            'spacing.portPort': 1.0,
        }
    }


def component_to_elk(c):
    return {
        'id': c.refdes,
        'ports': [pin_to_elk(p) for p in c.pins._get()],
        'properties': {
            'nodeSize.minimum': '(2, 2)',
            'nodeSize.constraints': '[PORTS, MINIMUM_SIZE]'
        }
    }


def pin_to_elk(pin):
    return {
        'id': pin.component.refdes + '.' + pin.name,
        'properties': {},
        'width': 2.0,
        'height': 1.0
    }


ELKJSON_PATH = os.path.join(
    os.path.dirname(__file__),
    'elkjson-0.1-jar-with-dependencies.jar')
ELKJSON_PACKAGE = 'layered'
ELKJSON_PROVIDER = 'LayeredLayoutProvider'


def run_elk(elk_input):
    input_file = tempfile.NamedTemporaryFile(delete=False)
    input_file.write(json.dumps(elk_input).encode('utf8'))
    input_file.close()

    output_file = tempfile.NamedTemporaryFile(delete=False)
    output_file.close()

    subprocess.run([
        'java', '-jar',
        ELKJSON_PATH,
        '-i', input_file.name,
        '-o', output_file.name,
        '-p', ELKJSON_PACKAGE,
        '-l', ELKJSON_PROVIDER],
        check=True)

    with open(output_file.name, 'rb') as f:
        output = f.read()

    try:
        os.remove(input_file.name)
        os.remove(output_file.name)
    except OSError:
        pass

    return json.loads(output)
