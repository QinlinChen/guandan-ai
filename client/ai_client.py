from .base_client import BaseClient
import random
import time
import client.utils as utils


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

        print('Choose', utils.action_to_str(action))
        return action

    def normal_strategy(self, env):
        if env.i_have_priority():
            return self.normal_strategy_with_priority(env)
        else:
            return self.normal_strategy_without_priority(env)

    def normal_strategy_with_priority(self, env):
        action = self.win_with_high_prob_strategy(env)
        if action:
            return action
        action = self.help_ally_strategy(env)
        if action:
            return action
        action = self.reduce_hand_cards_strategy(env)
        if action:
            return action
        action = self.resist_enemy_strategy(env)
        if action:
            return action
        return self.min_strategy(env)

    def win_with_high_prob_strategy(self, env):
        partition = utils.partition(env.hand_cards)
        if len(partition) == 1:
            card_type = list(partition.keys())[0]
            return self.min_strategy(env, card_type=card_type)
        if len(partition) in [2, 3]:
            fire_card = set(
                [card_type for card_type in partition if utils.is_fire_card])
            non_fire_card = set(
                [card_type for card_type in partition if not utils.is_fire_card])
            if len(fire_card) and len(non_fire_card):
                return self.min_strategy(env, card_type=non_fire_card.pop())
        return None

    def help_ally_strategy(self, env):
        ally_rest = env.rest_hand_cards(env.my_ally())
        if ally_rest == 1 and 'Single' in env.action_list:
            return self.min_strategy(env, card_type='Single')
        if ally_rest == 2 and 'Pair' in env.action_list:
            return self.min_strategy(env, card_type='Pair')
        return None

    def resist_enemy_strategy(self, env):
        enemy_rest = min(env.rest_hand_cards(env.my_next_player()),
                         env.rest_hand_cards(env.my_prev_player()))
        if enemy_rest == 1 and 'Pair' in env.action_list:
            return self.min_strategy(env, card_type='Pair')
        if enemy_rest == 2 and 'Single' in env.action_list:
            return self.min_strategy(env, card_type='Single')
        return None

    def reduce_hand_cards_strategy(self, env):
        if 'ThreeWithTwo' in env.action_list:
            return self.min_strategy(env, card_type='ThreeWithTwo')
        return None

    def normal_strategy_without_priority(self, env):
        # TODO
        return self.min_strategy(env)

    def tribute_strategy(self, env):
        return self.random_strategy(env, card_type='tribute')

    def back_strategy(self, env):
        return self.min_strategy(env, card_type='back')

    def random_strategy(self, env, card_type=None):
        if not card_type or card_type not in env.action_list:
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

    def min_strategy(self, env, card_type=None):
        if not card_type or card_type not in env.action_list:
            all_card_types = env.action_list.keys()
            card_type = min(all_card_types, key=utils.card_type_order)

        all_ranks = env.action_list[card_type].keys()
        min_rank = min(all_ranks, key=utils.rank_order)
        all_actions = list(env.action_list[card_type][min_rank])
        first_action = all_actions[0]

        return {
            'action': first_action,
            'type': card_type,
            'rank': min_rank
        }
