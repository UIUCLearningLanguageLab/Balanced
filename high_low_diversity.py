"""
Re-used code that first appeared here:
https://stackoverflow.com/questions/25285792/generate-all-permutations-of-a-list-without-adjacent-equal-elements

"""


import random
from typing import List, Any, Set, Tuple, Union
import itertools

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
    if count:
        yield from enum1([], count, sum(count.values()), get_mode(count))
    else:
        yield ()


def permute_but_not_repeat(seq):
    """randomly chose a permutation of "seq" in which no adjacent elements are identical """
    solutions = list(enum(seq))
    return random.choice(solutions)


def create_random_low_diversity_list(num_repetitions: int,
                                     offset: int,
                                     v1: Set[Any],
                                     v2: Set[Any],
                                     ) -> List[Tuple[Any, Any]]:
    """
    create a random sequence of samples from two finite sets,
    such that:
    1) any element occurs exactly "repetitions" times, and
    2) each element in "v1" is always paired with the same element from "v2",
    3) no adjacent elements (from var 1 or 2) are identical
    :param num_repetitions: number of times an item-pair is repeated
    :param offset: influences which element in variable 1 is paired to which element in variable 2
    :param v1: set of elements in first variable (e.g. words)
    :param v2: set of elements in second variable (e.g. images)
    :return: random list
    """

    if not len(v1) == len(v2):
        raise ValueError('All sets must have same length')

    # start by creating a valid sequence of elements from variable 1
    v1_solution = permute_but_not_repeat(list(v1) * num_repetitions)

    # define mapping between v1 and v2
    v1i2cycle = {v1i: itertools.cycle(v2i)
                 for v1i, v2i in itertools.filterfalse(lambda i: i[1] is None,
                                                       zip(itertools.cycle(sorted(v1)),
                                                           itertools.chain([None] * offset, v2)))}

    # pair each element in v1_solution with elements from v2
    res = []
    for v1i in v1_solution:
        res.append((v1i, next(v1i2cycle[v1i])))

    return res


def create_random_high_diversity_list(num_repetitions: int,
                                      v1: Set[Any],
                                      v2: Set[Any],
                                      ) -> List[Tuple[Any, Any]]:
    """
    create a random sequence of samples from two finite sets,
    such that:
    1) any element occurs exactly "repetitions" times, and
    2) each element in "v1" is paired with each element from "v2" equally often,
    3) no adjacent elements (from var 1 or 2) are identical
    :param num_repetitions: number of times an item-pair is repeated
    :param v1: set of elements in first variable (e.g. words)
    :param v2: set of elements in second variable (e.g. images)
    :return: random list
    """

    if not len(v1) == len(v2):
        raise ValueError('All sets must have same length')

    # start by creating a valid sequence of elements from variable 1
    v1_solution = permute_but_not_repeat(list(v1) * num_repetitions)

    # define mapping between v1 and v2
    v1i2cycle = {v1i: itertools.cycle(v2) for v1i in v1}

    # pair each element in v1_solution with elements from v2
    res = []
    for v1i in v1_solution:
        res.append((v1i, next(v1i2cycle[v1i])))

    return res


var1 = {'a', 'b', 'c', 'd'}
var2 = {'1', '2', '3', '4'}

print('low diversity:')
print(create_random_low_diversity_list(4, 0, var1, var2))
print(create_random_low_diversity_list(4, 1, var1, var2))
print(create_random_low_diversity_list(4, 2, var1, var2))
print(create_random_low_diversity_list(4, 3, var1, var2))

print('high diversity:')
print(create_random_high_diversity_list(4, var1, var2))
print(create_random_high_diversity_list(4, var1, var2))
print(create_random_high_diversity_list(4, var1, var2))
print(create_random_high_diversity_list(4, var1, var2))

