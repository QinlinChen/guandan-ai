from .base_client import BaseClient
import client.utils as utils


class MinClient(BaseClient):

    def __init__(self, name, addr, port, verbose, measure_time):
        super().__init__(name, addr, port, verbose, measure_time)

    def my_play(self, env):
        if self.verbose:
            print('------------------ my play ----------------------')
        action = self.min_strategy(env)
        if self.verbose:
            print('Choose', utils.action_to_str(action))
        return action
