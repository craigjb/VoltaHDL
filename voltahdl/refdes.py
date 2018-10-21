from . import blocks


def assign_block(block):
    components = blocks.flatten_components(block)
    refdes_counters, refdes_map = {}, {}
    # assign components with user-specified refdes first
    for comp in [c for c in components if c.refdes is not None]:
        assign_component(comp, refdes_counters, refdes_map)
    for comp in [c for c in components if c.refdes is None]:
        assign_component(comp, refdes_counters, refdes_map)


def assign_component(comp, refdes_counters, refdes_map):
    if comp.refdes is not None:
        if comp.refdes in refdes_map:
            raise RefDesError(
                'Refdes {} has been assigned to more than one component'
                .format(comp.refdes))
        else:
            refdes_map[comp.refdes] = comp
    else:
        prefix = comp.refdes_prefix
        while comp.refdes is None:
            index = refdes_counters.get(prefix, 0) + 1
            refdes_counters[prefix] = index
            refdes = prefix + str(index)
            if refdes not in refdes_map:
                refdes_map[refdes] = comp
                comp.refdes = refdes


class RefDesError(Exception):
    pass
