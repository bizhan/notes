# file: profile_speed.py

"""Profile the run time of a function with a decorator.
"""
import functools

import timeit                                                   #1

import pystone_converter                                        #2

speed = {}                                                      #3

def profile_speed(function):                                    #4
    """The decorator.
    """
    @functools.wraps(function)
    def _profile_speed(*args, **kwargs):                        #5
        """This replaces the original function.
        """
        start = timeit.default_timer()                          #6
        try:
            return function(*args, **kwargs)                    #7
        finally:
            # Will be executed *before* the return.
            run_time = timeit.default_timer() - start           #8
                                                                #9
            kstones = pystone_converter.kpystone_from_seconds(run_time)
            speed[function.__name__] = {'time': run_time,
                                        'kstones': kstones}     #10
    return _profile_speed                                       #11
