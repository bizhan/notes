"""Simple test function for line_profiler.
"""

@profile
def accumulate(iterable):
    """Accumulate the intermediate steps in summing all elements.

    The result is a list with the lenght of `iterable`.
    The last elments is the sum of all elements of `ieterable`
    >>>accumulate(range(5))
    [0, 1, 3, 6, 10]
    accumulate(range(10))
    [0, 1, 3, 6, 10, 15, 21, 28, 36, 45]
    """
    acm = [iterable[0]]
    for elem in iterable[1:]:
        old_value = acm[-1]
        new_value = old_value + elem
        acm.append(new_value)
    return acm


if __name__ == '__main__':
    accumulate(range(10))
    accumulate(range(100))
