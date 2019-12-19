import sys
from client import client_factory

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print('usage: {} <client_type> <name>'.format(sys.argv[0]))
        exit(0)

    try:
        ws = client_factory(sys.argv[1], sys.argv[2])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
