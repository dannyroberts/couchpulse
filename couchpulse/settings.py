from ConfigParser import ConfigParser

_parser = ConfigParser()
_parser.read('alembic.ini')

SQLALCHEMY_URL = _parser.get('alembic', 'sqlalchemy.url')
