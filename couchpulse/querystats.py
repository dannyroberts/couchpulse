from couchpulse import sql
from sqlalchemy import or_, func


def query_stats(session, columns):
    return session.query(*columns).outerjoin(
        sql.ResponseLog,
        sql.RequestLog.id == sql.ResponseLog.id
    )


def recent_flagged_queries(since_time, max_time, max_size, like=None, limit=None, aggregate=True):
    session = sql.Session()
    if not aggregate:
        keys = (
            'timestamp',
            'method',
            'path',
            'params',
            'req_size',
            'req_time',
            'res_time',
            'res_size',
        )
        columns = (
            sql.RequestLog.timestamp,
            sql.RequestLog.method,
            sql.RequestLog.path,
            sql.RequestLog.params,
            sql.RequestLog.size,
            sql.RequestLog.time,
            sql.ResponseLog.time,
            sql.ResponseLog.size,
        )
    else:
        keys = (
            'count',
            'method',
            'path',
            'req_size',
            'req_time',
            'res_time',
            'res_size',
        )
        columns = (
            func.count(sql.RequestLog.path),
            sql.RequestLog.method,
            sql.RequestLog.path,
            func.avg(sql.RequestLog.size),
            func.avg(sql.RequestLog.time),
            func.avg(sql.ResponseLog.time),
            func.avg(sql.ResponseLog.size),
        )
    query = query_stats(session, columns).filter(
        sql.RequestLog.timestamp > since_time,
        or_(
            sql.RequestLog.time > max_time,
            sql.RequestLog.time + sql.ResponseLog.time > max_time,
            sql.RequestLog.size + sql.ResponseLog.size > max_size,
            sql.ResponseLog.size > max_size,
        )
    )
    if like:
        query = query.filter(sql.RequestLog.path.like(like))
    if aggregate:
        query = query.group_by(
            sql.RequestLog.method,
            sql.RequestLog.path,
        ).order_by(func.avg(sql.RequestLog.time).desc())
    else:
        query = query.order_by(sql.RequestLog.time.desc())
        if limit:
            query = query.limit(limit)

    for row in query:
        row = dict(zip(keys, row))
        yield row
