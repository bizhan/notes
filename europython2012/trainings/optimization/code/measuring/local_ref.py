"""Testing access to local name and name refrenced on another module.
"""

import math

# If there is no decorator `profile`, make one that just calls the function,
# i.e. does nothing.
# This allows to call `kernprof` with and without the option `-l` without
# commenting or un-commentimg `@profile' all the time.
# You can add this to the builtins to make it availbale in the whole program.
try:
    @profile
    def dummy():
        """Needs to be here to avoid a syntax error.
        """
        pass
except NameError:
    def profile(func):
        """Will act as the decorator `profile` if it was alreday found.
        """
        def mock(*args, **kwargs):
            """Just call the function. No actual decoration effect.
            """
            return func(*args, ** kwargs)
        return mock


def local_ref(counter):
    """Access local name.
    """
    # make it local
    sqrt = math.sqrt
    for _ in xrange(counter):
        sqrt


def module_ref(counter):
    """Access name as attribute of another module.
    """
    for _ in xrange(counter):
        math.sqrt


@profile
def test(counter):
    """Call both functions.
    """
    local_ref(counter)
    module_ref(counter)

if __name__ == '__main__':
    test(int(1e8))
