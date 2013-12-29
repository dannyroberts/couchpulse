# couchpulse

A couchdb query logger for couchdbkit using apache kafka

External requirements (non-python):

- postgres
- kafka


## Quick Start

### Virtualenv

Assuming you have virtualenv installed

```bash
mkvirtualenv couchpulse
pip install -r requirements.txt
export PYTHONPATH=`pwd`
```

### Postgres setup
Assuming you have postgres installed,

```bash
createdb couchpulse
psql couchpulse
> CREATE EXTENSION IF NOT EXISTS hstore;
> \q
alembic upgrade head
```

### Start up Kafka

Download Kafka from http://kafka.apache.org/downloads.html (0.8.0+)

```bash
cd kafka/ # for me it was kafka_2.8.0-0.8.0/
bin/zookeeper-server-start.sh config/zookeeper.properties > zookeeper.log &
bin/kafka-server-start.sh config/server.properties > kafka-server.log &
```

### Monkey Patch

To monkey patch your code add the lines

```python
import couchpulse
couchpulse.monkey_patch()
```

to your entry point.


### Run the log reader

To have couchpulse read your logs (as a separate process) and store them in
postgres, run

```bash
python couchpulse.py readlogs
```

## Example Data

Example query on data once stored in postgres
(all queries in the last 10 minutes grouped by url and sorted by
cumulative amount of time spent processing the requests):

```
SELECT count(*), method, path, sum(req_size) AS req_size, sum(res_size) AS res_size, sum(req_time) AS req_time FROM querystats
WHERE timestamp > now() AT TIME ZONE 'utc' - interval '10 minutes' GROUP BY method, path ORDER BY req_time DESC;
 count | method |                                      path                                       | req_size | res_size |      req_time
-------+--------+---------------------------------------------------------------------------------+----------+----------+---------------------
     4 | GET    | http://127.0.0.1:5984/commcarehq/_design/adm/_view/all_default_reports          |          |       48 |  0.0206940174102783
     5 | GET    | http://127.0.0.1:5984/commcarehq/_design/users/_view/by_domain                  |          |     3717 |  0.0200099945068359
     4 | GET    | http://127.0.0.1:5984/commcarehq/_design/couchexport/_view/saved_export_schemas |          |      152 |  0.0125160217285156
     3 | GET    | http://127.0.0.1:5984/commcarehq/_design/app_manager/_view/applications_brief   |          |     2613 | 0.00965619087219238
     1 | GET    | http://127.0.0.1:5984/commcarehq/_design/cloudcare/_view/application_access     |          |       38 | 0.00808405876159668
     2 | GET    | http://127.0.0.1:5984/commcarehq/_design/groups/_view/by_domain                 |          |       76 | 0.00644326210021973
     2 | GET    | http://127.0.0.1:5984/commcarehq/_design/app_manager/_view/saved_app            |          |      881 | 0.00591492652893066
     1 | GET    | http://127.0.0.1:5984/commcarehq/_design/cloudcare/_view/cloudcare_apps         |          |      797 | 0.00588607788085938
     2 | GET    | http://127.0.0.1:5984/commcarehq/d0a0001cde20030b07e3ec34e6105c02               |          |    13826 | 0.00485491752624512
     1 | GET    | http://127.0.0.1:5984/commcarehq/_design/users/_view/by_username                |          |     1194 | 0.00331616401672363
(10 rows)

```
