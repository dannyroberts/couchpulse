from ConfigParser import ConfigParser, NoSectionError
import os

_parser = ConfigParser()
_filepath = os.path.join(
    os.path.dirname(__file__),
    '..',
    'alembic.ini'
)
_parser.read(_filepath)

try:
    SQLALCHEMY_URL = _parser.get('alembic', 'sqlalchemy.url')
except NoSectionError:
    SQLALCHEMY_URL = None

KAFKA_HOST = 'localhost'
KAFKA_PORT = 9092
KAFKA_TOPIC = 'couchpulse'

TIME_THRESHOLD = .500  # in seconds
SIZE_THRESHOLD = 1000000  # in bytes

try:
    from django.conf import settings
except ImportError:
    pass
else:
    from django.core.exceptions import ImproperlyConfigured
    try:
        KAFKA_HOST = getattr(settings, 'KAFKA_HOST', KAFKA_HOST)
        KAFKA_PORT = getattr(settings, 'KAFKA_PORT', KAFKA_PORT)
        KAFKA_TOPIC = getattr(settings, 'KAFKA_TOPIC', KAFKA_TOPIC)
        SQLALCHEMY_URL = getattr(settings, 'COUCHPULSE_DATABASE_URL',
                                 SQLALCHEMY_URL)
        TIME_THRESHOLD = getattr(settings, 'COUCHPULSE_TIME_THRESHOLD',
                                 TIME_THRESHOLD)
        SIZE_THRESHOLD = getattr(settings, 'COUCHPULSE_SIZE_THRESHOLD',
                                 SIZE_THRESHOLD)

    except (ImproperlyConfigured, ImportError):
        pass
