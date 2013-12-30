import json
import uuid
from couchdbkit import CouchdbResource
from couchdbkit.resource import CouchDBResponse, encode_params
from kafka.client import KafkaClient
from kafka.producer import SimpleProducer
import time
from couchpulse.models import RequestLog, ResponseLog


kafka_client = KafkaClient("localhost", 9092)
kafka_producer = SimpleProducer(kafka_client, "couchpulse")


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
        kafka_producer.send_messages(json.dumps(message))
        return value


_old_request = CouchdbResource.request


def logging_request(self, method, path=None, payload=None, headers=None, **params):
    tracking_number = str(uuid.uuid4())
    full_path = self.uri.rstrip('/') + '/' + path.lstrip('/')
    print full_path
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

    message = RequestLog(
        id=tracking_number,
        method=method,
        path=full_path,
        time=elapsed_time,
        timestamp=start_time,
        size=len(json.dumps(payload)) if payload else None,
        params=encode_params(params),
    ).to_json()
    kafka_producer.send_messages(json.dumps(message))

    # playin' it fast and loose!
    response._logging_info = (tracking_number, method, full_path)
    response.__class__ = LoggingResponse
    return response


def monkey_patch():
    CouchdbResource.request = logging_request