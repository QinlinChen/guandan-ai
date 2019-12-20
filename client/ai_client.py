from .base_client import BaseClient
import random
import time


class AIClient(BaseClient):

    def __init__(self, url,):
        super().__init__(url)

    def my_play(self, env):
        print('------------------ my play ----------------------')
        env.print_play_area()

        time.sleep(1)

        all_card_types = list(env.action_list.keys())
        card_type = random.choice(all_card_types)
        all_ranks = list(env.action_list[card_type].keys())
        rank = random.choice(all_ranks)
        all_actions = list(env.action_list[card_type][rank])
        action = random.choice(all_actions)

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

