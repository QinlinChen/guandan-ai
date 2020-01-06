from .human_client import HumanClient
from .random_client import RandomClient
from .ai_client import AIClient
from .min_client import MinClient


def client_factory(strategy, name, addr, port, verbose=0, measure_time=False):
    if strategy == 'random':
        return RandomClient(name, addr, port, verbose, measure_time)
    if strategy == 'human':
        return HumanClient(name, addr, port, verbose, measure_time)
    if strategy == 'min':
        return MinClient(name, addr, port, verbose, measure_time)
    if strategy == 'ai':
        return AIClient(name, addr, port, verbose, measure_time)
    raise ValueError('Invalid client type: {}'.format(strategy))
