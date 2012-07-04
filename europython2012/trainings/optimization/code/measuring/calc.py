"""Simple test function for line_profiler doing some math.
"""

import math


@profile
def calc(number, loops=1000):
    """Do some math calculations.
    """
    sqrt = math.sqrt
    for x in xrange(loops):
        x = number + 10
        x = number * 10
        x = number ** 10
        x = pow(x, 10)
        x = math.sqrt(number)
        x = sqrt(number)
        math.sqrt
        sqrt

if __name__ == '__main__':
    calc(100, int(1e5))
