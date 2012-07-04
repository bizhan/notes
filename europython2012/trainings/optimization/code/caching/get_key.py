# file: get_key.py
# based on Ziade 2008

"""Generate a unique key for a function and its arguments.
"""


def get_key(function, *args, **kw):                             #1
    """Make key from module and function names as well as arguments.
    """
    key = '%s.%s:' % (function.__module__,
                      function.__name__)                        #2
    hash_args = [str(arg) for arg in args]                      #3
    hash_kw = ['%s:%s' % (k, str(v))
               for k, v in kw.items()]                          #4
    return '%s::%s::%s' % (key, hash_args, hash_kw)             #5
