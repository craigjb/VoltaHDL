import re


def find_pins(pattern, component, prefilter=None):
    matches = []
    for pin in component.pins._get():
        if (prefilter is not None and
                not re.search(prefilter, pin.name, re.IGNORECASE)):
            continue
        if re.search(pattern, pin.name, flags=re.IGNORECASE):
            matches.append(pin)
    return matches


def find_pin(pattern, component, prefilter=None):
    matches = find_pins(pattern, component, prefilter)
    if len(matches) > 1:
        raise ValueError(
            'Multiple pins match pattern: ' + pattern)
    return matches[0] if len(matches) > 0 else None
