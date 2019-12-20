from .base_client import BaseClient
import random
import time


class RandomClient(BaseClient):

    def __init__(self, url):
        super().__init__(url)

    def my_play(self, env):
        print('------------------ my play ----------------------')
        env.print_play_area()

        all_card_types = list(env.action_list.keys())
        card_type = random.choice(all_card_types)
        all_ranks = list(env.action_list[card_type].keys())
        rank = random.choice(all_ranks)
        all_actions = list(env.action_list[card_type][rank])
        action = random.choice(all_actions)

        print('Choose {}:{}'.format(card_type, action))

        return {
            'action': action,
            'type': card_type,
            'rank': rank
        }

    def others_play(self, env):
        print('----------------- others play -------------------')
        env.print_play_area()
        print('Choose {}: {}'.format(
            env.action_performed['type'], env.action_performed['action']))

    def finish(self, env):
        print('-------------------- finish ---------------------')
        print('finish winners:', env.winners)
