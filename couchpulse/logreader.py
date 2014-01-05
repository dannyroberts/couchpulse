import json
import datetime
from kafka import KafkaClient
from kafka import SimpleConsumer

from . import models
from . import sql
import time
import sqlalchemy.exc

from couchpulse import settings

kafka_client = KafkaClient(settings.KAFKA_HOST, settings.KAFKA_PORT)
kafka_consumer = SimpleConsumer(kafka_client, 'couchpulse.logreader', settings.KAFKA_TOPIC, auto_commit=False)


def consume():
    session = sql.Session()
    for message in kafka_consumer:
        message = json.loads(message.message.value)
        if not message.get('id'):
            print ('skipping')
            continue
        type = message['type']
        if type == 'request':
            r = models.RequestLog(message)
            session.add(sql.RequestLog(
                id=r.id,
                method=r.method,
                path=r.path,
                params=r.params,
                size=r.size,
                time=r.time,
                timestamp=datetime.datetime.utcfromtimestamp(r.timestamp),
            ))
            print 'saving request %s (%s)' % (r.timestamp, r.id)
        elif type == 'response':
            r = models.ResponseLog(message)
            session.add(sql.ResponseLog(
                id=r.id,
                size=r.size,
                time=r.time,
            ))
            print 'saving response %s' % r.id
        try:
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            session.rollback()
    session.close()


def consume_forever():
    while True:
        consume()
        time.sleep(1)
