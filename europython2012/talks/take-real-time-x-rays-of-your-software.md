# Take real-time X-rays of your software for fun and performance
## by L. Almeida

Performance Debugging

- Prevention
  * Functional performance testing
    - `mechanize`
- __Before__ production
- Proactive Monitoring

With reproduction instructions

- `profile` and `cProfile`
  * Heavy performance toll
  * Complicated output
  * Show calls only, not lines
  * Way too slow for production
- `statprof`
  * Sampling of tracebacks -> statistics
  * More relevant info than `cProfile`
  * And lighter
  * Still doesn't "tell the story"

Without reproduction instructions

- Sprinkle timing calls
  * `log(time.time() - start_time)`
  * Time consuming...
  * On the production environment?!
- `DeadlockDebugger`

Quick Zope Primer

- Z Object Publishing Environment
- One listening thread
  * Parses HTTP Request
- A few Worker threads
  * `http://server/document/method?foo=bar` translates to `document.method(foo="bar")`
- ZODB: Object Oriented DB
  * Clusterable:
    - `ZEO`, `RelStorage`, `NEO`

`sys._get_current_frames()`

- Python dict
  * Key: thread id (`int`)
    - Same as `thread.get_ident()` for each thread
  * Value: Stack Frame
    - Currently executing frame on this thread
    - Tip of the thread's stack

Stack frame

- Currently executing Function
  * file name
  * line number
- Pointer to previous frame
- Variables
  * locals
  * globals
- ...

Proactive monitoring

- Parsing of HTTP server logs
  * Report slow URLs
  * Many "false" positives
- Still not enough info, just sprinkling timing calls
