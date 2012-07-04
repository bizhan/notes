Faster Python programs through Optimization
===========================================

Ask yourself: Do I need optimization?

Profiling
---------

From the stdlib:

- `profile` (a lot of overhead)
- `hotshot` (not recommended)
- `cProfile` (less overhead, use this!)
- `timeit` for timing (use `time.clock` on Windows machines for more precision)
- `pstats` for interpreting the results gathered by `cProfile`

Third-party tools:

- `RunSnakeRun` for visualizing the stats gathered by `cProfile`
- `line_profiler` allows line-by-line profiling

Memory profiling

- `heapy` tool from the Guppy PE framework (works for Py2.7 on trunk)
- `pympler` works on Py2.7

Algorithms and Anti-Patterns
----------------------------

String concatenation

- Strings in Python are inmutable, concatenating with `+` actually creates a
  new one.
- Use ''.join() for concatenation

List comprehensions

- If you throw away the list, you can use a generator expression
  (micro-optimization):

    sum(x * x for x in xrange(10))

    # instead of

    sum([x * x for x in xrange(10)])

Locals VS Globals

- Look-ups in the local namespace are faster than accessing globals and
  builtins. Not a big difference but you save some dictionary look-ups making
  frequently accesed globals and builtins local.

The Right Data Structure
------------------------

List VS Set

- If you need to search in items, dicts and sets are mostly preferable to
  lists. Set is considerably faster for large collections.

List VS collections.deque

- A `collections.deque` is a doubly linked list. Allows faster insertion into 
  the middle part but access of elements by index is slow.

dict VS collections.defaultdict

- `collections.defaultdict` allow you to set default factories for each key.

Big-O notation and Data Structures

- Is better to "append and reverse" than inserting values in the beggining of a
  list.

Caching
-------

If you find yourself calling the same function with the same arguments many
times then caching might help to improve the performance of your program.

Deterministic caching

- If we want to cache result, we need to uniquely identify the function we want 
  to call

Non-deterministic caching

- For non-deterministic caching, we use an age that the computed values should
  not exceed.

Memcached

- Caching server that is primarily used to speed up database based dynamic web
  pages.

Testing speed
-------------

- The `timeit` module is designed to check small pieces of code:

    $ python -mtimeit 'x=0' 'x+=1'

Psyco, the JIT
--------------

- Not developed any further, only available for 32-bit PC architecture and
  Python 2.6 or older

PyPy
----

- Implementation of Python 2.7 that is faster that the standard CPython
  implementation for many common tasks.

Numpy for Numeric Arrays
------------------------

- A library implemented in C that brings numerical processing to Python.

NumPyPy
-------

- Rewrite of Numpy in PyPy.
- Still incomplete.

Using Multiple CPUs with `multiprocessing`
------------------------------------------

- Threads in Python don't take advantage of multiple cores due to the GIL. The
  `multiprocessing` module allows use multiple processors.
