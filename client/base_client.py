from ws4py.client.threadedclient import WebSocketClient
from client.env import Env
import client.utils as utils
import json
import random


class BaseClient(WebSocketClient):

    def __init__(self, url,):
        super().__init__(url)
        self.env = Env()

    def closed(self, code, reason=None):
        print('Closed down', code, reason)

    def received_message(self, message):
        content = json.loads(str(message))
        self.env.see(content)

        # Dispatch event
        if self.env.type == 0:
            self.finish(self.env)
        elif self.env.type == 1:
            self.others_play(self.env)
        elif self.env.type in [2, 5, 6]:
            assert self.env.action_list
            action = self.my_play(self.env)
            action = self._verify_action(action)
            self.env.my_choice(action)
            self.send(json.dumps(action))
        else:
            raise AssertionError('Should not reach here')

    def _verify_action(self, action):
        if not action:
            raise ValueError('Invalid action')
        if action['type'] not in self.env.action_list:
            print('----------------------Warning-------------------------')
            print('The chosen type {} not in action list'.format(
                action['type']))
            print('Current state:')
            for player in range(4):
                print(self.env._mem.play_area(player),
                      'active:', self.env.is_active(player))
            print(self.env.action_list)
            # This warning is caused by some server's bugs
            return self.min_strategy(self.env)
        return action

    def my_play(self, env):
        return utils.pass_action()

    def others_play(self, env):
        pass

    def finish(self, env):
        pass

    # ----------------------------------------------------------
    #                     Basic Strategies
    # ----------------------------------------------------------
    def random_strategy(self, env, card_type=None):
        if not card_type or card_type not in env.action_list:
            all_card_types = list(env.action_list.keys())
            card_type = random.choice(all_card_types)

        all_ranks = list(env.action_list[card_type].keys())
        rank = random.choice(all_ranks)
        all_actions = list(env.action_list[card_type][rank])
        action = random.choice(all_actions)

        return {'type': card_type, 'rank': rank, 'action': action}

    def min_strategy(self, env, card_type=None):
        if not card_type or card_type not in env.action_list:
            if card_type and card_type not in env.action_list:
                print(card_type)
                print(env.action_list)
                assert False  # guard
            all_card_types = env.action_list.keys()
            card_type = min(all_card_types, key=utils.card_type_order)

        all_ranks = env.action_list[card_type].keys()
        min_rank = min(all_ranks, key=utils.rank_order)
        all_actions = list(env.action_list[card_type][min_rank])
        first_action = all_actions[0]

        return {'type': card_type, 'rank': min_rank, 'action': first_action}
