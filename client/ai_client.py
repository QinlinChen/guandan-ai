from .base_client import BaseClient
import random
import time


def rank_to_int(rank):
    map = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
        '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14,
        'JOKER': 15, 'PASS': 0
    }
    return map[rank]


class AIClient(BaseClient):

    def __init__(self, url):
        super().__init__(url)

    def my_play(self, env):
        print('------------------ my play ----------------------')

        if env.type == 2:
            action = self.normal_strategy(env)
        elif env.type == 5:
            action = self.tribute_strategy(env)
        elif env.type == 6:
            action = self.back_strategy(env)
        else:
            raise AssertionError('Should not reach here')

        print('choose {}: {}'.format(action['type'], action['action']))
        return action

    def normal_strategy(self, env):
        return self.random_strategy(env)

    def tribute_strategy(self, env):
        return self.random_strategy(env)

    def back_strategy(self, env):
        card_type = 'back'
        all_ranks = env.action_list[card_type].keys()
        min_rank = min(all_ranks, key=rank_to_int)
        all_actions = list(env.action_list[card_type][min_rank])
        action = random.choice(all_actions)
        return {
            'action': action,
            'type': card_type,
            'rank': min_rank
        }

    def random_strategy(self, env):
        all_card_types = list(env.action_list.keys())
        card_type = random.choice(all_card_types)
        all_ranks = list(env.action_list[card_type].keys())
        rank = random.choice(all_ranks)
        all_actions = list(env.action_list[card_type][rank])
        action = random.choice(all_actions)
        return {
            'action': action,
            'type': card_type,
            'rank': rank
        }

    def my_play_with_priority(self, env):
        pass

    def my_play_without_priority(self, env):
        pass
