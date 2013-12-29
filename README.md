# couchpulse

A couchdb query logger for couchdbkit using apache kafka

## Install

```bash
$ createdb couchpulse
$ psql couchpulse
> CREATE EXTENSION IF NOT EXISTS hstore;
> \q
$ export PYTHONPATH=`pwd`
$ alembic upgrade head
```

To monkey patch your code add the lines

```python
import couchpulse
couchpulse.monkey_patch()
```

to your entry point.

To have couchpulse read your logs (as a separate process) and store them in
postgres, run

```bash
python couchpulse.py readlogs
```
