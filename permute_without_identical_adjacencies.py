"""
Re-used code that first appeared here:
https://stackoverflow.com/questions/25285792/generate-all-permutations-of-a-list-without-adjacent-equal-elements

"""

import random
from collections import Counter
from operator import itemgetter


def get_mode(count):
    return max(count.items(), key=itemgetter(1))[0]


def enum2(prefix, x, count, total, mode):
    prefix.append(x)
    count_x = count[x]
    if count_x == 1:
        del count[x]
    else:
        count[x] = count_x - 1
    yield from enum1(prefix, count, total - 1, mode)
    count[x] = count_x
    del prefix[-1]


def enum1(prefix, count, total, mode):
    if total == 0:
        yield tuple(prefix)
        return
    if count[mode] * 2 - 1 >= total and [mode] != prefix[-1:]:
        yield from enum2(prefix, mode, count, total, mode)
    else:
        defect_okay = not prefix or count[prefix[-1]] * 2 > total
        mode = get_mode(count)
        for x in list(count.keys()):
            if defect_okay or [x] != prefix[-1:]:
                yield from enum2(prefix, x, count, total, mode)


def enum(seq):
    """generate all possible permutations of "seq" such that no adjacent elements can be identical"""
    count = Counter(seq)
    print('Enumerating all possible solutions...')
    if count:
        yield from enum1([], count, sum(count.values()), get_mode(count))
    else:
        yield ()


def pick_permutation_randomly(seq):
    """randomly chose a permutation of "seq" in which no adjacent elements are identical """
    solutions = list(enum(seq))
    return random.choice(solutions)