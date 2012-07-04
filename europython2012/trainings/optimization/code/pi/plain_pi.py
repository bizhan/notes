# file: plain_pi.py

"""Calculating pi with Monte Carlo.
"""

import math                                                     #1
import random
import sys

# make `import measure_time` work
sys.path.append('../measuring')
import measure_time                                             #2


def pi_plain(total):                                            #3
    """Calculate pi with `total` hits.
    """
    count_inside = 0                                            #4
    for _ in xrange(total):                                     #5
        x = random.random()                                     #6
        y = random.random()                                     #7
        dist = math.sqrt(x * x + y * y)                         #8
        if dist < 1:
            count_inside += 1                                   #9
    return 4.0 * count_inside / total                           #10

if __name__ == '__main__':                                      #11

    def test():
        """Check if it works.
        """
        print 'pi:', pi_plain(int(1e5))                         #12
        names = ['pi_plain']                                    #13
        total = int(1e5)                                        #14
        repeat = 5                                              #15
        measure_time.measure_run_time(total, names, repeat)     #16

    test()
