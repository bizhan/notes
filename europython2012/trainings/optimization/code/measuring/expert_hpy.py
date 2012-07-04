import time
import sys
from test import pystone
from guppy import hpy

benchtime, stones = pystone.pystones()

def secs_to_kstones(seconds):
    return (stones*seconds) / 1000 
stats = {}
if sys.platform == 'win32':
    timer = time.clock
else:
    timer = time.time
    
def profile(name='stats', stats=stats):
    """Calculates a duration and a memory size."""
    def _profile(function):
        def __profile(*args, **kw):
            start_time = timer()
            profiler = hpy()
            profiler.setref()
            # 12 corresponds to the initial memory size
            # after a setref call
            start = profiler.heap().size + 12
            try:
                return function(*args, **kw)
            finally:
                total = timer() - start_time
                kstones = secs_to_kstones(total)
                memory = profiler.heap().size - start
                stats[name] = {'time': total, 
                               'stones': kstones, 

                               'memory': profiler.heap().size}
        return __profile
    return _profile

def eat_memory():
    memory = []
    def _get_char():
        return chr(random.randint(97, 122))
    for i in range(10):
        size = random.randint(20, 150)
        data = [_get_char() for i in xrange(size)]
        memory.append(''.join(data))
    return '\n'.join(memory)

if __name__ == '__main__':
    import random

    eat_it = profile('you bad boy!')(eat_memory)
    please = eat_it()
    print stats