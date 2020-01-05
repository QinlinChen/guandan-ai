from .base_client import BaseClient
import client.utils as utils
from client.stop_watch import StopWatch


class RandomClient(BaseClient):

    def __init__(self, url):
        super().__init__(url)
        self._stop_watch = StopWatch('random')

    def my_play(self, env):
        print('------------------ my play ----------------------')
        self._stop_watch.begin()
        action = self.random_strategy(env)
        self._stop_watch.end()
        print('Choose', utils.action_to_str(action))
        self._stop_watch.print()
        return action
