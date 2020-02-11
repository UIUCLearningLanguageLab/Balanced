import random


def all_same(items):
    return all(x == items[0] for x in items)


def create_random_list(num: int, *vs):
    """
    create a random sequence of samples from an arbitrary number of finite sets,
    such that no two neighboring samples contain overlapping elements.
    :param num: length of sequence
    :param vs: list of finite sets
    :return: random list
    """

    # check that sets have same length
    if not all_same([len(v) for v in vs]):
        raise ValueError('All sets must have same length')

    res = [[random.choice(list(v)) for v in vs]]
    for _ in range(num):
        sample = []
        for vn, v in enumerate(vs):
            sample.append(random.choice([vi for vi in v if vi != res[-1][vn]]))
        res.append(sample)

    return res


var1 = {'a', 'b', 'c', 'd'}
var2 = {'1', '2', '3', '4'}
var3 = {'@', '#', '&', '-'}

print(create_random_list(16, var1, var2))
print(create_random_list(16, var1, var2, var3))
