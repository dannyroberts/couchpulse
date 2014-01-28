import datetime

from celery.task import task
import sqlalchemy.exc
from celery.utils.log import get_task_logger

from . import models
from . import sql

logger = get_task_logger(__name__)


@task
def consume_message(message):
    session = sql.Session()
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
            traceback=r.traceback,
        ))
        logger.info('saving request %s (%s)' % (r.timestamp, r.id))
    elif type == 'response':
        r = models.ResponseLog(message)
        session.add(sql.ResponseLog(
            id=r.id,
            size=r.size,
            time=r.time,
        ))
        logger.info('saving response %s' % r.id)
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
    session.close()
