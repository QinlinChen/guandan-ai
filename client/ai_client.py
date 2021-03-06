from .base_client import BaseClient
import client.utils as utils


class AIClient(BaseClient):

    def __init__(self, name, addr, port, verbose, measure_time):
        super().__init__(name, addr, port, verbose, measure_time)

    def my_play(self, env):
        if self.verbose:
            print('------------------ my play ----------------------')

        if env.type == 2:
            action = self.normal_strategy(env)
        elif env.type == 5:
            action = self.tribute_strategy(env)
        elif env.type == 6:
            action = self.back_strategy(env)
        else:
            raise AssertionError('Should not reach here')

        if self.verbose:
            prefix_map = {2: 'Play', 5: 'Tribute', 6: 'Back'}
            print(prefix_map[env.type], utils.action_to_str(action))

        return action

    # ----------------------------------------------------------
    #               Nomral Playing Strategies
    # ----------------------------------------------------------

    def normal_strategy(self, env):
        # action, unsafe = self.ending_strategy(env)
        # if action:
        #    return action
        if env.i_have_priority():
            return self.normal_strategy_with_priority(env)
        else:
            return self.normal_strategy_without_priority(env)

    def ending_strategy(self, env):
        next_enemy_left_cards_n = env.rest_hand_cards(env.my_next_player())
        ally_left_cards_n = env.rest_hand_cards(env.my_ally())
        if next_enemy_left_cards_n == 1 or next_enemy_left_cards_n == 2:
            return None, True
        if ally_left_cards_n == 1:
            action = self.min_strategy(env, 'Single')
            if action:
                return action, False
            return None, False
        if ally_left_cards_n == 2:
            action = self.min_strategy(env, 'Pair')
            if action:
                return action, False
            return None, False
        return None, False

    def normal_strategy_with_priority(self, env):
        action = self.win_with_high_prob_strategy(env)
        if action:
            return action
        action = self.help_ally_strategy_with_priority(env)
        if action:
            return action
        action = self.reduce_hand_cards_strategy_with_priority(env)
        if action:
            return action
        action = self.resist_enemy_strategy_with_priority(env)
        if action:
            return action
        return self.min_strategy(env)

    def win_with_high_prob_strategy(self, env):
        partition = utils.partition(env.hand_cards)
        if len(partition) == 1:
            card_type = list(partition.keys())[0]
            return self.min_strategy(env, card_type=card_type)
        if len(partition) in [2, 3]:
            fire_card = set([card_type for card_type in partition
                             if utils.is_fire_card(card_type)])
            non_fire_card = set([card_type for card_type in partition
                                 if not utils.is_fire_card(card_type)])
            if len(fire_card) and len(non_fire_card):
                return self.min_strategy(env, card_type=non_fire_card.pop())
        return None

    def help_ally_strategy_with_priority(self, env):
        ally_rest = env.rest_hand_cards(env.my_ally())
        if ally_rest == 1 and 'Single' in env.action_list:
            return self.min_strategy(env, card_type='Single')
        if ally_rest == 2 and 'Pair' in env.action_list:
            return self.min_strategy(env, card_type='Pair')
        return None

    def resist_enemy_strategy_with_priority(self, env):
        enemy_rest = min(env.rest_hand_cards(env.my_next_player()),
                         env.rest_hand_cards(env.my_prev_player()))
        if enemy_rest == 1 and 'Pair' in env.action_list:
            return self.min_strategy(env, card_type='Pair')
        if enemy_rest == 2 and 'Single' in env.action_list:
            return self.min_strategy(env, card_type='Single')
        return None

    def reduce_hand_cards_strategy_with_priority(self, env):
        if 'ThreeWithTwo' in env.action_list:
            return self.min_strategy(env, card_type='ThreeWithTwo')
        return None

    def normal_strategy_without_priority(self, env):
        action = self.help_ally_strategy_without_priority(env)
        if action:
            return action

        partition = set(utils.partition(env.hand_cards).keys())
        available = set(env.action_list.keys())
        p_and_a = partition.intersection(available)

        last_card_type = env.last_card_type()
        assert last_card_type
        if last_card_type in p_and_a:
            return self.min_strategy(env, last_card_type)
        if not p_and_a:
            return self.min_strategy(env)
        if 'Bomb' in p_and_a:
            last_card_rank = env.last_card_rank()
            assert last_card_rank
            if utils.rank_cmp(last_card_rank, '10') > 0:
                return self.min_strategy(env, 'Bomb')
        # print('we pass, but min strategy is: ', utils.action_to_str(self.min_strategy(env)))
        # print('last card type and rank:', env.last_card_type(), env.last_card_rank())
        # print('hand cards:', env.hand_cards)
        return utils.pass_action()

    def help_ally_strategy_without_priority(self, env):
        if not env.is_active(env.my_ally()):
            return None
        ally_action = env.play_area(env.my_ally())
        if utils.is_fire_card(ally_action['type']):
            return utils.pass_action()
        if utils.rank_cmp(ally_action['rank'], 'K') >= 0:
            return utils.pass_action()
        return None

    # ----------------------------------------------------------
    #                Tribute and Back Strategies
    # ----------------------------------------------------------
    def tribute_strategy(self, env):
        return self.random_strategy(env, card_type='tribute')

    def back_strategy(self, env):
        return self.min_strategy(env, card_type='back')
