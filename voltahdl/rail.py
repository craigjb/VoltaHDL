from voltahdl import circuit


class Rail(object):
    def __init__(self, p, n):
        super().__init__()

        self.p = circuit.net_for(p)
        self.n = circuit.net_for(n)

    def __lt__(self, other):
        self.n + other
