"""Local vs. built-in.
"""


def repeat(counter):
    """Using the built-in `True` in a loop.
    """
    for count in xrange(counter):
        True


def repeat_local(counter):
    """Making `True` a local variable.
    """
    true = True
    for count in xrange(counter):
        true


def test(counter):
    """Call both functions.
    """
    repeat(counter)
    repeat_local(counter)


if __name__ == '__main__':

    def do_profile():
        """Check the run times.
        """
        import cProfile
        profiler = cProfile.Profile()
        profiler.run('test(int(1e8))')
        profiler.print_stats()

    do_profile()
