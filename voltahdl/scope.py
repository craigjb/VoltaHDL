SCOPE_STACK = []


def push(circuit):
    SCOPE_STACK.append(circuit)


def pop():
    return SCOPE_STACK.pop()
