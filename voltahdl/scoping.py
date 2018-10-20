from . import block


SCOPE_STACK = [block.Block()]


def current_block():
    return SCOPE_STACK[-1]


def pop_block():
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
