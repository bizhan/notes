# file: memory_size_hpy.py

"""Measure the size of used memory with a decorator.
"""

import functools                                                #1

from guppy import hpy                                           #2

memory = {}                                                     #3


def measure_memory(function):                                   #4
    """Decorator to measure memory size.
    """

    @functools.wraps(function)                                  #5
    def _measure_memory(*args, **kwargs):                       #6
        """This replaces the function that is to be measured.
        """
        measurer = hpy()                                        #7
        measurer.setref()                                       #8
        inital_memory = measurer.heap().size                    #9
        try:
            res = function(*args, **kwargs)                     #10
            return res
        finally:                                                #11
            memory[function.__name__] = (measurer.heap().size -
                                         inital_memory)
    return _measure_memory                                      #12


if __name__ == '__main__':

    @measure_memory                                             #13
    def make_big(number):
        """Example function that makes a large list.
        """
        return range(number)                                         #14

    make_big(int(1e6))                                          #15
    print 'used memory', memory                                 #16
