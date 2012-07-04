# file pool_pi.py

"""Multiprocessing with a pool of workers.
"""

import math
try:
    from multiprocessing import Pool, cpu_count                  #1
except ImportError:
    from processing import Pool, cpu_count                       #2
import random
import timeit


def count_inside(total):
    """Count the hits inside the circle.

    This function will be run multiple times in different
    processes.
    """
    inside_count = 0
    for _ in xrange(total):
        x = random.random()
        y = random.random()
        dist = math.sqrt(x * x + y * y)
        if dist < 1:
            inside_count += 1
    return inside_count


def calc_pi(total):
    """Determine pi _without_ multprocessing as refrence.
    """
    return 4 * count_inside(total) / float(total)


def calc_pi_workers(total, workers=None):                           #3
    """Calculate pi spread of several processses with workers.

    We need to split the task into sub tasks before we can hand
    them to other process that run workers
    """
    if not workers:
        workers = cpu_count()                                  #4
    min_n = total // workers
    counters = [min_n] * workers
    reminder = total % workers
    for count in xrange(reminder):
        counters[count] += 1
    pool = Pool(processes=workers)                              #5
    results = [pool.apply_async(count_inside, (counter,))
                       for counter in counters]                 #6
    inside_count = sum(result.get() for result in results)      #7
    return 4 * inside_count / float(total)                      #8

if __name__ == '__main__':

    def test():
        """Check if it works.
        """
        workers = 2

        total = int(1e3)

        print 'number of tries: %2.0e' % total
        start = timeit.default_timer()
        print 'pi:', calc_pi(total)
        no_time = timeit.default_timer() - start
        print 'run time no workers:', no_time

        start = timeit.default_timer()
        pi_value = calc_pi_workers(total, workers)
        print 'pi', pi_value
        two_time = timeit.default_timer() - start
        print 'run time %d workers:' % workers, two_time
        print 'ratio:', no_time / two_time
        print 'diff:', two_time - no_time

    test()
