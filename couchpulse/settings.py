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
