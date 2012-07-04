# file: cache_deterministic.py
# form Ziade 2008

"""Example for a deterministic cache
"""

import functools


from get_key import get_key                                     #1

cache = {}                                                      #2


def memoize_deterministic(get_key=get_key, cache=cache):         #3
    """Parameterized decorator for memoizing.
    """

    def _memoize(function):                                     #4
        """This takes the function.
        """

        @functools.wraps(function)
        def __memoize(*args, **kw):                             #5
            """This replaces the original function.
            """
            key = get_key(function, *args, **kw)                #6
            try:
                return cache[key]                               #7
            except KeyError:
                value = function(*args, **kw)                   #8
                cache[key] = value                              #9
                return value                                    #10
        return __memoize
    return _memoize
