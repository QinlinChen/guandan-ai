from .base_client import BaseClient
import client.utils as utils
import random
import time


class RandomClient(BaseClient):

    def __init__(self, url):
        super().__init__(url)

    def my_play(self, env):
        print('------------------ my play ----------------------')

        all_card_types = list(env.action_list.keys())
        card_type = random.choice(all_card_types)
        all_ranks = list(env.action_list[card_type].keys())
        rank = random.choice(all_ranks)
        all_actions = list(env.action_list[card_type][rank])
        action = random.choice(all_actions)

        result = {'action': action, 'type': card_type, 'rank': rank}
        print('Choose', utils.action_to_str(result))
        return result
