from .human_client import HumanClient
from .random_client import RandomClient
from .ai_client import AIClient
from .min_client import MinClient

def client_factory(client_type, name, ip='127.0.0.1', port='23456'):
    url = 'ws://{}:{}/game/{}'.format(ip, port, name)
    if client_type == 'random':
        return RandomClient(url)
    if client_type == 'human':
        return HumanClient(url)
    if client_type == 'min':
        return MinClient(url)
    if client_type == 'ai':
        return AIClient(url)
    raise ValueError('Invalid client type: {}'.format(client_type))
