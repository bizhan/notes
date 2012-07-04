#file: pool_numpy_pi.py

"""Combining NumPy and multiprocessing.
"""

try:
    from multiprocessing import Pool, cpu_count
except ImportError:
    from processing import Pool, cpu_count

import numpy


def count_inside(total):                                        #1
    """Count hits inside the circle.
    """
    x = numpy.random.rand(total)
    y = numpy.random.rand(total)
    dist = numpy.sqrt(x * x + y * y)
    return len(numpy.where(dist < 1)[0])                        #2


def calc_pi(total):
    """Calcualte pi from the hits inside and the total hits.
    """
    return 4 * count_inside(total) / float(total)


def calc_pi_workers_numpy(total, workers=None):
    """Spread the work over several processes.
    """
    if not workers:
        workers = cpu_count()
    min_n = total // workers
    counters = [min_n] * workers
    reminder = total % workers
    for count in xrange(reminder):
        counters[count] += 1
    pool = Pool(processes=workers)
    results = [pool.apply_async(count_inside, [counter])
                       for counter in counters]
    inside_count = sum(result.get() for result in results)
    return 4 * inside_count / float(total)

if __name__ == '__main__':

    def test():
        """Run some performamce tests.
        """
        import timeit

        workers = 2

        total = int(1e3)

        print 'number of tries: %2.0e' % total
        start = timeit.default_timer()
        print 'pi:', calc_pi(total)
        no_time = timeit.default_timer() - start
        print 'run time no workers:', no_time

        start = timeit.default_timer()
        pi_value = calc_pi_workers_numpy(total, workers)
        print 'pi', pi_value
        two_time = timeit.default_timer() - start
        print 'run time %d workers:' % workers, two_time
        print 'ratio:', no_time / two_time
        print 'diff:', two_time - no_time

    test()
