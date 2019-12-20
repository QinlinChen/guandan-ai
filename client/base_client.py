import json
from enum import Enum
from ws4py.client.threadedclient import WebSocketClient
import client.utils as utils


class EnvState(Enum):
    PREPARE = 0
    PALY = 1


class PersistentMem():

    def __init__(self):
        super().__init__()
        self.refresh()

    def refresh(self):
        self.cards = []
        self.play_area = [{
            'action': [[0, 'PASS']],
            'type': 'PASS',
            'rank': 'PASS'
        }] * 4
        self.my_id = -1

    def record_cards(self, action):
        # TODO: record cards
        pass

    def query_has_larger(self, action):
        pass

    def set_my_play_area(self, action):
        assert self.my_id != -1
        self.play_area[self.my_id] = action

    def set_play_area(self, player, action):
        self.play_area[player] = action


class Env:

    def __init__(self):
        self._state = EnvState.PREPARE
        self.mem = PersistentMem()

    def see(self, content):
        if content['type'] not in [0, 1, 2, 5, 6]:
            raise ValueError('Invalid content type: {}'.format(content))
        self.type = content['type']

        if self._state == EnvState.PREPARE:
            if self.type == 0:
                raise ValueError('Should not receive message type 0')
            self.mem.refresh()
            self._state = EnvState.PALY
        elif self._state == EnvState.PALY:
            if self.type == 0:
                self._state = EnvState.PREPARE
        else:
            raise AssertionError('Should not reach here')

        self._parse(content)

    def my_choice(self, action):
        self.mem.set_my_play_area(action)
        self.mem.record_cards(action)

    def _parse(self, content):
        if self.type == 0:
            self.winners = content['winners']
        else:
            self.hand_cards = content['hand_cards']
            self.public = content['public']
            self.current_rank = content['current_rank']
            self.current_player = content['current_player']
            self.action_list = content['action_list']
            self.action_performed = content['action_performed']

            if self.type == 1:
                self.mem.set_play_area(
                    self.current_player, self.action_performed)
                self.mem.record_cards(self.action_performed)
            elif self.type in [2, 5, 6]:
                self.mem.my_id = self.current_player

    def print_play_area(self):
        for player in range(4):
            prefix = '*' if player == self.current_player else ' '
            play_area = self.mem.play_area[player]
            print('{} {}({}): {}'.format(
                prefix, player, self.rest_hand_cards(player),
                utils.action_to_str(play_area)))

    def my_id(self):
        return self.mem.my_id

    def my_ally(self):
        return utils.ally_player(self.mem.my_id)

    def my_next_player(self):
        return utils.next_player(self.mem.my_id)

    def my_prev_player(self):
        return utils.next_player(self.mem.my_id)

    def i_have_priority(self):
        assert self.mem.my_id == self.current_player
        for player in range(4):
            if player != self.mem.my_id:
                if self.mem.play_area[player]['type'] != 'PASS':
                    return False
        return True

    def rest_hand_cards(self, player):
        return self.public[player]['rest']


class BaseClient(WebSocketClient):

    def __init__(self, url,):
        super().__init__(url)
        self.env=Env()

    def closed(self, code, reason = None):
        print('Closed down', code, reason)

    def received_message(self, message):
        content=json.loads(str(message))
        self.env.see(content)

        # dispatch event
        if self.env.type == 0:
            self.finish(self.env)
        elif self.env.type == 1:
            self.others_play(self.env)
        elif self.env.type in [2, 5, 6]:
            assert self.env.action_list
            action=self.my_play(self.env)
            if not action:
                raise ValueError('Invalid action')
            self.env.my_choice(action)
            self.send(json.dumps(action))
        else:
            raise AssertionError('Should not reach here')

    def my_play(self, env):
        return {}

    def others_play(self, env):
        pass

    def finish(self, env):
        pass
