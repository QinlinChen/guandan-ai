import json
from ws4py.client.threadedclient import WebSocketClient


class HumanClient(WebSocketClient):

    def __init__(self, url,):
        super().__init__(url)

    def closed(self, code, reason=None):
        print('Closed down', code, reason)

    def received_message(self, message):
        content = json.loads(str(message))

        print('--------------------------------------------------------')
        print('message type {}'.format(content['type']))
        for i in range(0, 4):
            print(self._card_mem.play_area(i))

        if 'action_list' in content and content['action_list']:
            action = self._human_play(content['action_list'])
            self.send(json.dumps(action))
            print('Choose action:', action)

    def _human_play(self, action_list):
        all_card_types = list(action_list.keys())
        card_type = _input_from_choices(all_card_types, 'input card type: ')

        all_ranks = list(action_list[card_type].keys())
        rank = _input_from_choices(all_ranks, 'input rank: ')

        all_actions = list(action_list[card_type][rank])
        action = _input_from_choices(all_actions, 'input action: ')

        return {
            'action': action,
            'type': card_type,
            'rank': rank
        }


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
