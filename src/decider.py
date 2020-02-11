import random


class Decider:
    """decide which element from options to pair with element from variable 1"""
    def __init__(self, v1i, options):
        self.v1i = v1i
        self.check = options.copy()
        self.options = options.copy()
        self.right_adjacent_deciders = []  # other deciders that come after current decider

    def pick(self, last_v2i=None):
        """pick element from options to be paired with element from variable 1"""
        if last_v2i is not None:
            assert last_v2i in self.check

        # get next decider in sequence, and if next decider only has 1 option, then disallow this option here
        try:
            next_d = self.right_adjacent_deciders.pop(0)
        except IndexError:  # avoid getting next adjacent decider when current decider is last in sequence
            next_v2i = last_v2i
        else:
            if len(next_d.options) == 1:
                next_v2i = next_d.options[0]  # we know this option should never be chosen
            else:
                next_v2i = None

        # get options that are bad but not impossible (this helps bring error down from 50% to 10%
        bad = []
        for d in self.right_adjacent_deciders:
            bad.extend([o for o in self.check if o not in d.options])

        # these options should never be chosen
        never = {last_v2i, next_v2i}
        # print(sorted(self.options), [last_v2i, next_v2i], sorted(set(bad)))

        # make a decision (a guess, really based on some local knowledge)
        choices = [o for o in self.options if o not in never and o not in bad]
        if not choices:  # we must include bad options now
            choices = [o for o in self.options if o not in never]
            # print('choices including bad options', choices)
        option = random.choice(choices)

        # option cannot be chosen again (high diversity means each v1 element is always paired with a different v2)
        self.options.remove(option)
        # print(option)

        return option