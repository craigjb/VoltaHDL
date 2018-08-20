from . import scope


SIMULATIONS = []


def simulation(description):
    def simulation_decorator(f):
        SIMULATIONS.append((description, f))

        def wrapper(*args, **kwargs):
            scope.begin_scope()
            f(*args, **kwargs)
            scope.end_scope()

        return wrapper
    return simulation_decorator
