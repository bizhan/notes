# file: pystone_converter.py

"""Convert seconds to kilo pystones."""

from test import pystone

BENCHMARK_TIME, PYSTONES = pystone.pystones()


def kpystone_from_seconds(seconds):
    """Convert seconds to kilo pystones."""
    return (seconds * PYSTONES) / 1e3

if __name__ == '__main__':

    def test():
        """Show how it works
        """
        print
        print '%10s %10s' % ('seconds', 'kpystones')
        print
        for seconds in [0.1, 0.5, 1.0, 2.0, 5.0]:
            print ('%10.5f %10.5f' % (seconds, kpystone_from_seconds(seconds)))

    test()
