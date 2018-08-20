from functools import reduce
import copy


class Scope(object):
    def __init__(self):
        self.components = set()
        self.node_nets = dict()


SCOPES = [Scope()]


def current():
    return SCOPES[-1]


def begin():
    SCOPES.append(copy.copy(current()))


def end():
    if len(SCOPES) > 1:
        SCOPES.pop()
    else:
        raise RuntimeError('Cannot pop root scope')


def add_component(c):
    SCOPES[-1].components.add(c)
