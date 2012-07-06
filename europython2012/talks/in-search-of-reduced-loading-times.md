# In search of Reduced Loading Times (with Django)
## by Apostolis Bessas

### Optimizing SQL

- Measure
  * `django-debug-toolbar`
  * `django-devserver`
  * `django.db.backends.logger`
  * Database logging
    - `log_min_duration_statement` in PostgreSQL
- Evaluations

        qs = TodoItem.objects.filter(owner__username='me')
        nitems = qs.count()

        # CAUTION! The query gets evaluated TWICE

        return render_to_response(
            'template.html',
            {'nitems': nitems,
             'item': qs},
             context_instance=RequestContext(request)
        )

- Less queries
  * `select_related()` for `OneToOneField` and `ForeignKeyField`
  * `prefetch_related()`

`select_related`

        User.objects.select_related('profile').filter(username='mpessas').query

`prefetch_related`

        Pizza.objects.all().prefetch_related('toppings')

`.iterator()`

- Don't cache database results unnecessarily

`annotate`

- Use `values()` before `annotate()`

Raw SQL

- Don't be afraid to use raw SQL queries
  * `Manager.raw()`
  * `django.db.connection.cursor`

`RawQuerySet`

- `QuerySet`-like, but is **not** a `QuerySet`
- Generated objects are valid models
- Allows for complex queries

`defer()` and `only()`

- `defer`: columns to omit from the `SELECT` list
- `only`: columns to specify in the `SELECT` list

Bulk operations

- `bulk_create`
- `django-bulk`
- `COPY` (for PostgreSQL)
- Take advantage of the native features of your database

Denormalization

- Optimize read performance of a database by adding redundant data or by
  grouping data
- Mostly for read-only data

`Meta.Options.ordering`

- Don't use that

I/O

- Threads for I/O
- Async I/O

PJAX

- `django-pjax`

### Caching

Sessions

- Don't hit the database for sessions (Django does it by default)

Template compilation

- `django.template.loaders.cached.Loader`

Entity tags/Last-Modified Dates

- Allow to use browser cache (304 HTTP status code)
- Worth, only if easier to calculate
- What about *personalized* pages?
