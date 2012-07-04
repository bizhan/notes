PostgreSQL for Python programmers
==================================

- user-definable types
- full-text search

A single server can manage multiple databases. The whole group on a single
server is called a "cluster".

Commands
--------

`initdb` initializes a cluster, creates the files that will hold the DB. It
does not automatically start the server.

`pg_ctl` starts and stops PostgreSQL.

`psql` command-line interface to PostgreSQL.

Directories
-----------

All of the data lives under a top-level directory. The data lives in `base`.
The transaction logs live in `pg_xlog/`.

Lets call it $PGBASE.

Configuration
-------------

On most installations, the configuration files live in $PGBASE.

- postgresql.conf are the server settings
- pg_hba.conf  is the "Client Authentication Configuration file"
  * rules apply in a top-down fashion

postgresql.conf
~~~~~~~~~~~~~~~
- Most settings just require a server reload to take effect. 
- Some require a full server restart (such as `shared_buffers`).
- Many can be set on a per-session basis.

Important parameters:
- logging

Be generous with logging; it's very low-impact on the system.

Where to log?

syslog -- If you have a syslog infrastructure
standard format to files -- If you are using tools that need standard format.
otherwise, CSV format to files.

WHat to log?

    log_destination = 'csvlog'
    log_directory = 'pg_log'
    logging_colector = on                       # log rotator
    log_filename = 'postgres-%Y-%m-%d_%H%M%S'
    log_rotation_age = 1d                       # 1 day
    log_rotation_size = 1GB
    log_min_duration_statement = 250ms
    log_checkpoints = on
    log_connections = on
    log_disconnections = on
    log_lock_waits = on
    log_temp_files = 0                          # log every temporary file

- memory

Tweak these:

  * shared_buffers

    - Size
      <2GB => 20% of memory
      <32GB => 25% of memory
      >32GB => ~8GB

    - PostgreSQL allocates all shared memory at startup

  * work_mem

    - Start low: 32-64MB
    - Look for 'temporary file' lines in logs
    - Set to 2-3x the largest temp file you see
    - Can cause a **huge** speed-up if set properly!

  * maintenance_work_mem

    - 10% of system memory, up to 1GB
    - Maybe even higher if you are having VACUUM problems

  * effective_cache_size

    - Set to the amount of file system cache available
    - If you don't know, set it to 50% of total system memory

- checkpoints

  * A complete flush of dirty buffers to disk.
  * Potentially a lot of I/O
  * Done when the first of two thresholds are hit:
    - A particular number of WAL segments have been written
    - A timeout occurs


        wal_buffers = 16MB
        checkpoint_completion_target = 0.9
        checkpoint_timeout = <10m-30m>      # depends on restart time
        checkpoint_segments = 32            # to start

  * Look for checkpoint entries in the logs
  * Happening more often than `checkpoint_timeout`?
    - Adjust `checkpoint_segments` so that checkpoints happend due to timeouts
      rather than filling segments.
  * The WAL can take up to 3 x 16MB x `checkpoint_segments` on disk
  * Restarting PostgreSQL can take up to `checkpoint_timeout` (usually less)

- planner

  * `effective_io_concurrency` -- set to the number of I/o channes; otherwise,
    ignore it
  * `random_page_cost` -- 3.0 for a typical RAID10 array, 2.0 for a SAN, 1.1
    for Amazon EBS

Do not touch:

- fsync = on
  * Never change it
- synchronous_commit = on
  * Change this, but only if you understand the data loss potential

Users and Roles
---------------

A "role" is a databse object that can own other objecsts (tables, etc.) and has
priviliges. A "user" is just a role tha can log in to the system.

Security system base around users.

Concepts
--------

MVCC: Multi-Version Concurrency Control. 

Introduced by PostgreSQL, now used by pretty much everyone. Alternative to 
"pessimistic" locking strategies. 

Allows for higher performance. Readers (to the same row) do not block readers. Writers
do not block readers -- readers get the old version of the row. Readers do not
block writer. Writers to the same row **do** block.

Multiple versions of the same row can exist. Deleted and uptaded rows are not
immediately removed from the database.

VACUUM: Scans each table for "dead" versions of tuples, and marks them as free.
Good to manually vacuum after major update/delete operations.

ANALYZE: The planner requires statistics on each table to make good guesses for
how to execute queries. ANALYZE collects these statistics. Done as part of
VACUUM. Always do it after major database changes -- specially a restore from a
backup.

Locking: PostgreSQL takes implicit locks on objects to maintain concurrency
control.

Transactions

Multiple transaction modes:
 - READ COMMITTED
 - REPEATABLE READ
 - SERIALIZABLE

Schema design
-------------

- Keep your data in normal form.
- Do not be afraid to do joins

Fast/slow rule

- Do not put fast changing data in the same table as slow changing date
  * Especially if the table is the parent of a lot of other tables via FKs
- This will avoid a large class of locking problems

Indexing strategy

- A good index is:
  * Highly selective (queries return low number of records)
  * Frequently used
  * Or required to enforce a constraint

- A bad index:
  * Everything else

Index creation

- Create indexes on the basis of real-life queries
- Look for sequential scans that can be sped up
- Indexes are not cheap

Checking index usage

- pg_stat_user_tables
- pg_stat_user_indexes

Pitfalls
--------

SELECT COUNT(*) FROM ...
 - Implemented as a full table scan
 - Don't do this

In-place upgrade

- Upgrading major versions (9.0 => 9-1) requires a `pg_dump` and `pg_restore`
- `pg_upgrade

autovacuum

- Background process that does VACUUMing
- Handles most workloads well
- Sometimes can wake up at the wrong time`
  * Manual VACUUM
    - Disable AUTOVACUUM
    - ...

Bulk loading data

- Use COPY, not INSERT
- psycopg2 has a very nice COPY interface
- COPY does full integrity checking and trigger processing
- Do a VACUUM afterwards

Debugging
---------

Slow queries

- EXPLAIN or EXPLAINANALIZE
- Cryptic output
- Nice representation of EXPLAIN output => http://explain.depesz.com

Slow DBs

- `pg_stat_activity`
- `tail -f` the logs
- Too much I/O? `iostat 5`

The database isn't responding

- Make sure it's up!
- Can you connect with psql?
- `pg_stat_activity`
- `pg_locks`

Replication
-----------

Options

- Built-in streaming replication
- Trigger-based replication
  * Slony
  * Bucardo
  * Londiste

Built-in replication

- Available in the core
- Read/write master
- Read-only secondaries
- Single-level tree of secondaries to one master

Advantages

- Very fast
- Secondaries can be queried (load balancing)
- DDL changes are automatically pushed to secondaries

The bad news

- All-or-nothing: entire DB cluster
- Any change is immediately propagated
- Requires tuning for query cancellation issues

Trigger-based replication

- Installs triggers on tables on master
- A daemon process picks up the changes and applies them to the secondaries
- Third-party add-ons to PostgreSQL
- Highly configurable
- Don't have to replicate everything
- Multi-master setups possible (Bucardo)
- Fiddly and complex to set up
- Schema changes must be pushed out manually
- Overhead on the master

Pooling, etc.
-------------

Why pooling?

- Opening a connection to PostgreSQL is expensive
- It can easily be longer than the actual query time
- Above 200-300 connections, use a pooler

pgbouncer

- Developed by Skype
- Easy to install
- Very fast, can handle 1000s of connections
- Does not to failover, load-balancing
  * Use HAProxy or similar

pgpool II

- Does query analysis
- Can route queries between master and secondary in replication pairs
- Can do load balancing, failover, and secondary promotion
- Higher overhead, more complex to configure

Backup
------

pg_dump

- Built-in dump/restore tool
- Takes a logical snapshot of the database
- Does not lock the database or prevent writes to disk
- Low (but not zero) load on the database

pg_restore

- Restores database from a `pg_dump`
- Is not a fast operation
- Great for simple backups, not suitable for fast recovery from major failures

Point-in-time recovery

- Combine file-system level snapshot of the DB with archives of the WAL file
- File system snapshot does not need to be atomic or consistent
- Can be used to recover to a particular point-in-time in case of logical-level
  failures

Tools
-----

Monitoring

- Use Nagios/Ganglia to monitor
  * Disk space -- at minimum
  * CPU/Memory usage
  * Replication lag
- check_postgres.pl (http://bucardo.org)

Graphical clients

- pgAdmin III
  * Comprehensive, open-source

Log analysis

- pgFouine
  * Traditional, not maintained much anymore
  * Requires a patch for 9.1 log files
- pgbadger
  * Brand new, actively maintained

Books
-----

Title: PostgreSQL 9.0 High Performance
Author: Gregory Smith
