from .base_client import BaseClient
import client.utils as utils


def _gen_choice_list(choices):
    s = '\n'.join(['{}. {}'.format(i, choice)
                   for i, choice in enumerate(choices)])
    return s + '\n'


def _input_from_choices(choices, prompt=None):
    choice_list = _gen_choice_list(choices)
    if prompt:
        choice_list += prompt

    if len(choices) == 1:
        print(choice_list, '0')
        return choices[0]

    index = int(input(choice_list))
    if index >= len(choices):
        index = 0
    return choices[index]


class HumanClient(BaseClient):

    def __init__(self, url):
        super().__init__(url)

    def my_play(self, env):
        print('------------------ my play ----------------------')
        env.print_play_area()

        all_card_types = list(env.action_list.keys())
        card_type = _input_from_choices(all_card_types, 'input card type: ')
        all_ranks = list(env.action_list[card_type].keys())
        rank = _input_from_choices(all_ranks, 'input rank: ')
        all_actions = list(env.action_list[card_type][rank])
        action = _input_from_choices(all_actions, 'input action: ')

        result = {
            'action': action,
            'type': card_type,
            'rank': rank
        }
        print('Choose', utils.action_to_str(result))
        return result

    def others_play(self, env):
        print('----------------- others play -------------------')
        env.print_play_area()

    def finish(self, env):
        print('-------------------- finish ---------------------')
        print('finish winners:', env.winners)
