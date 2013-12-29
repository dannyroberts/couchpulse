import sys
from couchpulse import logreader

if __name__ == '__main__':
    command = sys.argv.pop()
    if command == 'readlogs':
        logreader.consume_forever()
