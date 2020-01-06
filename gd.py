import argparse
from client import client_factory


def parse_args():
    parser = argparse.ArgumentParser(description='Guandan Client Launcher')
    parser.add_argument('name',
                        help='set the client\'s name')
    parser.add_argument('-s', '--strategy', default='ai',
                        choices=['ai', 'random', 'min', 'human'],
                        help='choose the strategy')
    parser.add_argument('-a', '--addr', default='127.0.0.1',
                        help='set server\'s ip address')
    parser.add_argument('-p', '--port', default='23456',
                        help='set server\'s port')
    parser.add_argument('-t', '--time', action='store_true',
                        help='measure the time consumed by method call')
    parser.add_argument('-v', '--verbose', action="count", default=0,
                        help='show more infomation')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    try:
        ws = client_factory(args.strategy, args.name, args.addr, args.port,
                            verbose=args.verbose, measure_time=args.time)
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
