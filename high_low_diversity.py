from typing import List, Any, Set, Tuple
import itertools

from decider import Decider
from permute_without_identical_adjacencies import pick_permutation_randomly


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
    3) no adjacent elements (from var 1) are identical
    :param num_repetitions: number of times an item-pair is repeated
    :param offset: influences which element in variable 1 is paired to which element in variable 2
    :param v1: set of elements in first variable (e.g. words)
    :param v2: set of elements in second variable (e.g. images)
    :return: random list
    """

    if not len(v1) == len(v2):
        raise ValueError('All sets must have same length')

    # create a sequence of elements from variable 1 such that no adjacent elements are repeated
    v1_solution = pick_permutation_randomly(list(v1) * num_repetitions)

    # define mapping between v1 and v2
    v1i2cycle = {v1i: itertools.cycle(v2i)
                 for v1i, v2i in itertools.filterfalse(lambda i: i[1] is None,
                                                       zip(itertools.cycle(sorted(v1)),
                                                           itertools.chain([None] * offset, v2)))}

    # pair each element in v1_solution with elements from v2.
    # because v1 element is always paired with same v2 element,
    # this guarantees that no adjacent v2 elements are identical
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
    3) no adjacent elements (from var 1) are identical
    :param num_repetitions: number of times an item-pair is repeated
    :param v1: set of elements in first variable (e.g. words)
    :param v2: set of elements in second variable (e.g. images)
    :return: random list
    """

    if not len(v1) == len(v2):
        raise ValueError('All sets must have same length')

    # create a sequence of elements from variable 1 such that no adjacent elements are repeated
    v1_solution = pick_permutation_randomly(list(v1) * num_repetitions)

    # each identical element in v1_solution is assigned same Decider instance:
    # the Decider ensures that no identical element in v1_solution is paired more than once with element from var 2
    v1i2decider = {v1i: Decider(v1i, list(v2)) for v1i in v1}
    deciders = [v1i2decider[v1i] for v1i in v1_solution]

    # pair elements from v1 solution with elements from var 2, such that no adjacent var 2 elements are identical
    res = []
    for n, decider in enumerate(deciders):
        excluded = res[-1][1] if res else None
        sample = (decider.v1i, decider.pick(excluded))
        res.append(sample)

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

