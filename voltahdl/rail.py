from voltahdl import nets


class Rail(object):
    def __init__(self, p, n):
        super().__init__()

        self.p = nets.net_for(p)
        self.n = nets.net_for(n)

    def __lt__(self, other):
        self.n + other
