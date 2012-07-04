# file: memory_size_pympler.py

"""Measure the size of used memory with a decorator.
"""

import functools                                                #1

from pympler import tracker                                     #2

memory = {}                                                     #3


def measure_memory(function):                                   #4
    """Decorator to measure memory size.
    """

    @functools.wraps(function)                                  #5
    def _measure_memory(*args, **kwargs):                       #6
        """This replaces the function that is to be measured.
        """
        measurer = tracker.SummaryTracker()                     #7
        for _ in xrange(5):                                     #8
            measurer.diff()                                     #9
        try:
            res = function(*args, **kwargs)                     #10
            return res
        finally:                                                #11
            memory[function.__name__] = (measurer.diff())
    return _measure_memory                                      #12


if __name__ == '__main__':

    @measure_memory                                             #13
    def make_big(number):
        """Example function that makes a large list.
        """
        return xrange(number)                                    #14

    make_big(int(1e6))                                          #15
    print 'used memory', memory                                 #16
