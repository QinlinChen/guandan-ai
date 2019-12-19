import random
import time
from .base_client import BaseClient

def _random_from_choices(choices):
    return random.choice(choices)

class RandomClient(BaseClient):

    def __init__(self, url):
        super().__init__(url)

    def my_play(self, env):
        print('------------------ my play ----------------------')
        self.env.print_play_area()

        time.sleep(5)

        action_list = env.action_list
        all_card_types = list(action_list.keys())
        card_type = _random_from_choices(all_card_types)
        all_ranks = list(action_list[card_type].keys())
        rank = _random_from_choices(all_ranks)
        all_actions = list(action_list[card_type][rank])
        action = _random_from_choices(all_actions)

        print('Choose action:', action)

        return {
            'action': action,
            'type': card_type,
            'rank': rank
        }

    def others_play(self, env):
        print('----------------- others play -------------------')
        print(env.action_performed)
        env.print_play_area()
    
    def finish(self, env):
        print('-------------------- finish ---------------------')
        print('finish winner:', env.winner)
