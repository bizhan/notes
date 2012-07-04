# file: pympler_list_growth.py

"""Measure the size of a list as it grows.
"""

from pympler.asizeof import asizeof, flatsize


def list_mem(lenght, size_func=flatsize):
  """Measure incremental memory increase of a growing list.
  """
  my_list= []
  mem = [size_func(my_list)]
  for elem in xrange(lenght):
    my_list.append(elem)
    mem.append(size_func(my_list))
  return mem


if __name__ == '__main__':
  SIZE = 1000
  SHOW = 20
  import sys
  for func in [flatsize, asizeof, sys.getsizeof]:
    mem = list_mem(SIZE, size_func=func)
    try:
      from matplotlib import pylab
      pylab.plot(mem)
      pylab.show()
    except ImportError:
      print 'matplotlib seems not be installed. Skipping the plot.'
      if SIZE > SHOW:
        limit = SHOW / 2
        print mem[:limit], '... skipping %d elements ...' % (SIZE - SHOW),
        print mem[-limit:]
      else:
        print mem