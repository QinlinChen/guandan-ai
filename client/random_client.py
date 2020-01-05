from .base_client import BaseClient
import client.utils as utils


class RandomClient(BaseClient):

    def __init__(self, url):
        super().__init__(url)

    def my_play(self, env):
        print('------------------ my play ----------------------')
        action = self.random_strategy(env)
        print('Choose', utils.action_to_str(action))
        return action
