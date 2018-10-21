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
        'id': c.__class__.__name__,
        'ports': [pin_to_elk(p) for p in c.pins._get()],
        'properties': {
            'nodeSize.minimum': '(2, 2)',
            'nodeSize.constraints': '[PORTS, MINIMUM_SIZE]'
        }
    }


def pin_to_elk(pin):
    return {
        'id': pin.name,
        'properties': {},
        'width': 2.0,
        'height': 1.0
    }
