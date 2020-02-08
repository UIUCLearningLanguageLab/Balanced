import random


class Decider:
    """decide which element from options to pair with element from variable 1"""
    def __init__(self, v1i, options):
        self.v1i = v1i
        self.options = options.copy()

    def pick(self, e=None):
        """pick element from options to be paired with element from variable 1"""
        if e is not None and e in self.options:
            self.options.remove(e)

        random.shuffle(self.options)
        option = self.options.pop()

        if e is not None:
            self.options.append(e)
        return option


def pair_2_vars_without_identical_adjacency(seq, v1, v2):
    v1i2decider = {v1i: Decider(v1i, v2) for v1i in v1}

    # traverse decision path
    deciders = [v1i2decider[v1i] for v1i in seq]
    res = []
    for n, decider in enumerate(deciders):
        print(decider.v1i)

        excluded = res[-1][1] if res else None
        sample = (decider.v1i, decider.pick(excluded))
        res.append(sample)

    return res
