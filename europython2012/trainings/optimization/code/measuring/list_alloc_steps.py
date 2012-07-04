# file: list_alloc_steps.py

"""Measure the number of memory allocation steps for a list.
"""

import sys

from pympler.asizeof import flatsize


def list_steps(lenght, size_func=sys.getsizeof):
    """Measure the number of memory alloaction steps for a list.
    """
    my_list = []
    steps = 0
    int_size = size_func(int())
    old_size = size_func(my_list)
    for elem in xrange(lenght):
        my_list.append(elem)
        new_size = sys.getsizeof(my_list)
        if new_size - old_size > int_size:
            steps += 1
        old_size = new_size
    return steps


if __name__ == '__main__':
    print 'Using sys.getsizeof:'
    for size in [10, 100, 1000, 10000, int(1e5), int(1e6), int(1e7)]:
        print '%10d: %3d' % (size, list_steps(size))
    print 'Using pympler.asizeof.flatsize:'
    for size in [10, 100, 1000, 10000, int(1e5), int(1e6), int(1e7)]:
        print '%10d: %3d' % (size, list_steps(size, flatsize))
