# file: measure_time.py

"""Measure the run time of functions.
"""

from timeit import Timer                                    #1


def measure_run_time(total, names, number=1):               #2
    """Measure the run times of all functions given with `names`.
    """

    def timeit_runner(name):                                #3
        """Time one function.
        """
        timer = Timer('%s(total)' % name,
                      'from __main__ import %s\ntotal=%d'
                      % (name, total))                      #4
        return timer.timeit(number), name                   #5

    results = []                                            #6
    for name in  names:
        results.append(timeit_runner(name))                 #7
    results.sort()                                          #8
    length = max(len(name) for name in (names))             #9
    format1 = '%%-%ds' % length
    header = (format1 + '%s%10s') % ('Function',
                                     'Time'.center(11), 'Ratio')
    print
    print header
    print '=' * len(header)
    for result in results:
        ratio = result[0] / results[0][0]
        print (format1 + '%9.4f s%10.2f') % (result[1],
                                             result[0], ratio)

if __name__ == '__main__':

    import time

    def func1(total):
        """Test function that waits for `total` seconds.
        """
        time.sleep(total)

    def func2(total):
        """Test function that waits for `total` * 2 seconds.
        """
        time.sleep(total * 2)

    def test():
        """Check if it works.
        """
        measure_run_time(1, ['func1', 'func2'])

    test()
