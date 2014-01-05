from ConfigParser import ConfigParser
import os

_parser = ConfigParser()
_filepath = os.path.join(
    os.path.dirname(__file__),
    '..',
    'alembic.ini'
)
_parser.read(_filepath)

SQLALCHEMY_URL = _parser.get('alembic', 'sqlalchemy.url')

KAFKA_HOST = 'localhost'
KAFKA_PORT = 9092
KAFKA_TOPIC = 'couchpulse'

try:
    from django.conf import settings
except ImportError:
    pass
else:
    KAFKA_HOST = getattr(settings, 'KAFKA_HOST', KAFKA_HOST)
    KAFKA_PORT = getattr(settings, 'KAFKA_PORT', KAFKA_PORT)
    KAFKA_TOPIC = getattr(settings, 'KAFKA_TOPIC', KAFKA_TOPIC)
