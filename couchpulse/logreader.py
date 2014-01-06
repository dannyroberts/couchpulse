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


def consume(kafka_consumer):
    session = sql.Session()
    for kafka_message in kafka_consumer:
        message = json.loads(kafka_message.message.value)
        print kafka_message.offset,
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
    return kafka_consumer.offsets


def consume_forever(offsets=None, cache=None):
    kafka_consumer = SimpleConsumer(kafka_client, 'couchpulse.logreader', settings.KAFKA_TOPIC, auto_commit=False)
    if cache and offsets is None:
        offsets = cache.get('couchpulse.offsets')
    if offsets:
        print 'starting at offsets {0}'.format(offsets)
        kafka_consumer.offsets = offsets
        print kafka_consumer.offsets
    while True:
        offsets = consume(kafka_consumer)
        if cache and offsets:
            cache.set('couchpulse.offsets', offsets)
        time.sleep(1)
