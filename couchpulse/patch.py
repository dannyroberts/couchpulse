from cStringIO import StringIO
import json
import logging
import traceback
import uuid
import time

from couchdbkit import CouchdbResource
from couchdbkit.resource import CouchDBResponse, encode_params

from . import settings
from .models import RequestLog, ResponseLog
from .logreader import consume_message


def send_message(message):
    consume_message.delay(message)


class LoggingResponse(CouchDBResponse):

    def body_string(self, charset=None, unicode_errors="strict"):
        start_time = time.time()
        value = super(LoggingResponse, self).body_string(
            charset=charset,
            unicode_errors=unicode_errors,
        )
        end_time = time.time()
        elapsed_time = end_time - start_time
        tracking_number, method, path = self._logging_info
        message = ResponseLog(
            id=tracking_number,
            path=path,
            method=method,
            size=len(value),
            time=elapsed_time,
        ).to_json()
        send_message(message)
        return value


def get_traceback(limit):
    f = StringIO()
    traceback.print_stack(file=f, limit=15 + limit)
    lines = f.getvalue().strip().split('\n')
    count = 2
    for line in reversed(lines[:-2 * count]):
        if not line.lstrip().startswith("File"):
            continue
        elif '/restkit/' in line or '/couchdbkit/' in line:
            count += 1
        else:
            break

    end = -2 * count
    start = -2 * (count + limit)

    return "{traceback}\n[plus {skipped} other frames]".format(
        traceback='\n'.join(lines[start:end]),
        skipped=count,
    )


_old_request = CouchdbResource.request


def logging_request(self, method, path=None, payload=None, headers=None, **params):
    start_time = time.time()
    response = _old_request(
        self,
        method=method,
        path=path,
        payload=payload,
        headers=headers,
        **params
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    if isinstance(payload, str):
        size = len(payload)
    elif isinstance(payload, unicode):
        size = len(payload.encode('utf-8'))
    else:
        size = len(json.dumps(payload)) if payload else None
    if elapsed_time > settings.TIME_THRESHOLD or size > settings.SIZE_THRESHOLD:
        try:
            tb = get_traceback(limit=7)
        except Exception:
            logging.exception('Error retrieving traceback. Aborting.')
            tb = None

        try:
            tracking_number = str(uuid.uuid4())
            full_path = self.uri.rstrip('/') + '/' + path.lstrip('/')

            message = RequestLog(
                id=tracking_number,
                method=method,
                path=full_path,
                time=elapsed_time,
                timestamp=start_time,
                size=size,
                params=encode_params(params),
                traceback=tb,
            ).to_json()

            send_message(message)
        except Exception:
            logging.exception('Error during couchpulse logging. Aborting.')
        else:
            # playin' it fast and loose!
            response._logging_info = (tracking_number, method, full_path)
            response.__class__ = LoggingResponse
    return response


def monkey_patch():
    CouchdbResource.request = logging_request
