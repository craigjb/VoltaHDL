from . import blocks


SCOPE_STACK = [blocks.Block()]


def top_block():
    return SCOPE_STACK[0]


def current_block():
    return SCOPE_STACK[-1]


def pop_block():
    if len(SCOPE_STACK) == 1:
        raise ScopeError("Cannot pop top scope.")
    return SCOPE_STACK.pop()


def push_block(b):
    if b.parent is not None:
        raise ScopeError('This Block is already part of another Blockk.')
    current_block().children.add(b)
    b.parent = current_block()
    SCOPE_STACK.append(b)


def block(f):
    def block_wrapper():
        b = block.Block()
        push_block(b)
        f(b)
        pop_block()
        return b

    return block_wrapper


class ScopeError(Exception):
    pass
