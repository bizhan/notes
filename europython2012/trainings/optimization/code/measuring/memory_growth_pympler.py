# file memory_growth_pympler.py

"""Measure the memory growth during a function call.
"""

from pympler import tracker                                     #1


def check_memory_growth(function, *args, **kwargs):             #2
    """Measure the memory usage of `function`.
    """
    measurer = tracker.SummaryTracker()                         #3
    for _ in xrange(5):                                         #4
        measurer.diff()                                         #5    
    function(*args, **kwargs)                                   #6
    return measurer.diff()                                      #7

if __name__ == '__main__':

    def test():
        """Do some tests with different memory usage patterns.
        """

        def make_big(number):                                   #8
            """Function without side effects.

            It cleans up all used memory after it returns.
            """
            return range(number)

        data = []                                               #9

        def grow(number):
            """Function with side effects on global list.
            """
            for x in xrange(number):
                data.append(x)                                  #10
        size = int(1e6)
        print 'memory make_big:', check_memory_growth(make_big,
                                                      size)     #11
        print 'memory grow:', check_memory_growth(grow, size)   #12

    test()
