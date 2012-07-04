# Healthy Webapps Through Continuous Introspection
## by N. Venegas from the BitBucket team

Agenda

- Performance problems that may not be evident during development
- Common causes and their consequences
- Libraries to help
  * `dogslow`, `geordie` and `interruptingcow`

Wasted cycles on BitBucket

- SSH connection: -> sshd -> conq (Python) -> git/hg
- `conq` is our custom shell
  * finds the repo in the DB/filesystem
  * imports Django ORM and BitBucket code
  * takes ~1.41 seconds to start the script (spawns ~50 connections/s)
- Solution: no dependencies/imports and use plain SQL
  * drastycally reduced CPU usage
  * 60% load decrease on all web servers
  * 16 times faster to start up (0.09s vs 1.41s)

Slowness in Web Apps

- Slow (or too many) SQL queries
- Lock contention:
  * between threads
  * DB table/row locks
  * file locks (git/hg)
- Excesive IO (disk/network)
- Evil regex: r'^(a+)+$)'

Consequences

- 503 -- worker pool full
- 500 -- if request times out (Gunicorn sends `SIGKILL` to the process)
  * is best avoided as it destroys forensic evidence

`dogslow`

- Django middleware
- No performance penalty, safe on production
- Emails traceback of slow requests

`django-geordi`

- Selectively profile individual requests
- Add `?__geordi__` to any URL to enable the `VisorMiddleware` (accessible to
  admin users only)
- Produces PDF call graph
- Run outside the worker pool without timeouts (`celeryd`)

`interruptingcow`

- Time-box chunks of code
- Context manager for timeouting blocks of code
- Fail in a controlled manner, ensuring proper cleanup

Nested timeouts

- Time-box smaller chunks of code within a request
- Some part of the request is optional
  * BitBucket *linkers* that hyperlink commit messages

Summary

- [dogslow](https://bitbucket.org/evzijst/dogslow) -- tracebacks of slow requests
- [geordi](https://bitbucket.org/brodie/geordi) -- profiles production environments
- [interruptingcow](https://bitbucket.org/evzijst/interruptingcow) -- prevents slowness and fail gracefully
