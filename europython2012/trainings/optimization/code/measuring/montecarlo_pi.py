# file: montecarlo_pi.py

#!/usr/bin/env python

"""Test runner for all implementations.
"""

import sys

sys.path.append('../pi')                                        #1
sys.path.append('../multiprocessing')

has_psyco = False
try:
    import psyco                                                #2
    has_psyco = True
except ImportError:
    print 'No psyco found doing tests without it.'

has_numpy = False
try:
    import numpy                                                #3
    has_numpy = True
except ImportError:
    print 'No numpy found doing tests without it.'


import measure_time                                             #4

from plain_pi import pi_plain                                   #5
from math_pi import pi_math
from pool_pi import calc_pi_workers
if has_numpy:
    from numpy_pi import pi_numpy
    from pool_numpy_pi import calc_pi_workers_numpy


if has_psyco:
    psyco_pi_plain = psyco.proxy(pi_plain)                      #6
    psyco_pi_math = psyco.proxy(pi_math)
    psyco_calc_pi_workers = psyco.proxy(calc_pi_workers)
    if has_numpy:
        psyco_pi_numpy = psyco.proxy(pi_numpy)
        psyco_calc_pi_workers_numpy = psyco.proxy(calc_pi_workers_numpy)


def main():
    """Run all tests that could be found.
    """
    total = int(float(sys.argv[1]))                             #7
    repeat = int(sys.argv[2])                                   #8
    names = ['pi_plain', 'pi_math', 'calc_pi_workers']          #9
    if has_numpy:
        names.extend(['pi_numpy', 'calc_pi_workers_numpy'])     #10
    if has_psyco:
        names.extend(['psyco_pi_plain', 'psyco_pi_math',        #11
                      'psyco_calc_pi_workers'])
        if has_numpy:
            names.extend(['psyco_pi_numpy',
                          'psyco_calc_pi_workers_numpy'])       #12
    measure_time.measure_run_time(total, names, repeat)         #13


if __name__ == '__main__':

    main()
