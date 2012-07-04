# file: cache_non_deterministic.py
# form Ziade 2008

"""Example for a cache that expires.
"""

import functools
import time

from get_key import get_key

cache = {}

def memoize_non_deterministic(get_key=get_key, storage=cache,
                             age=0):                            #1
    """Parameterized decorator that takes an expiration age.
    """
    
    def _memoize(function):
        """This takes the function.
        """

        @functools.wraps(function)
        def __memoize(*args, **kw):
            """This replaces the original function.
            """
            key = get_key(function, *args, **kw)
            try:
                value_age, value = storage[key]                 #2
                deprecated = (age != 0 and 
                             (value_age + age) < time.time())   #3
            except KeyError:
                deprecated = True                               #4
            if not deprecated:
                return value                                    #5
            storage[key] = time.time(), function(*args, **kw)   #6
            return storage[key][1]                              #7
        return __memoize
    return _memoize
