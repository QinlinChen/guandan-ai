from .base_client import BaseClient
import client.utils as utils
from enum import Enum


def _gen_choice_list(choices):
    lines = ['{}. {}'.format(i, choice) for i, choice in enumerate(choices)]
    return '\n'.join(lines) + '\n'


def _input_from_choices(choices, prompt=None):
    choice_list = _gen_choice_list(choices)
    if prompt:
        choice_list += prompt

    index = input(choice_list)
    try:
        index = int(index)
    except:
        index = 0
    return index


class State(Enum):
    CHOOSE_TYPE = 1
    CHOOSE_RANK = 2
    CHOOSE_ACTION = 3


class HumanClient(BaseClient):

    def __init__(self, name, addr, port, verbose, measure_time):
        super().__init__(name, addr, port, verbose, measure_time)

    def my_play(self, env):
        print('------------------ my play ----------------------')
        env.print_play_area()

        state = State.CHOOSE_TYPE
        while True:
            if state == State.CHOOSE_TYPE:
                all_card_types = list(env.action_list.keys())
                choice = _input_from_choices(all_card_types, 'input card type: ')
                if choice == -1:
                    continue
                card_type = all_card_types[choice]
                state = State.CHOOSE_RANK
            elif state == State.CHOOSE_RANK:
                all_ranks = list(env.action_list[card_type].keys())
                choice = _input_from_choices(all_ranks, 'input rank: ')
                if choice == -1:
                    state = State.CHOOSE_TYPE
                    continue
                rank = all_ranks[choice]
                state = State.CHOOSE_ACTION
            elif state == State.CHOOSE_ACTION:
                all_actions = list(env.action_list[card_type][rank])
                choice = _input_from_choices(all_actions, 'input action: ')
                if choice == -1:
                    state = State.CHOOSE_RANK
                    continue
                action = all_actions[choice]
                break

        result = {'action': action, 'type': card_type, 'rank': rank}
        print('Choose', utils.action_to_str(result))
        return result

    def others_play(self, env):
        print('----------------- others play -------------------')
        env.print_play_area()

    def finish(self, env):
        print('-------------------- finish ---------------------')
        print('finish winners:', env.winners)
