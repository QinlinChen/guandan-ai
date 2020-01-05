import client.utils as utils
from enum import Enum


class EnvState(Enum):
    PREPARE = 0
    NORMAL_PLAY = 1
    TRIBUTE_OR_BACK = 2


class PersistentMem():

    def __init__(self):
        super().__init__()
        self.refresh()

    def refresh(self):
        self._cards = {}
        self._max_rank = {}
        self._play_area = [utils.pass_action()] * 4
        self._my_id = -1
        self._active = [False] * 4

    def my_id(self):
        return self._my_id

    def set_my_id(self, id):
        self._my_id = id

    def is_active(self, player):
        return self._active[player]

    def set_active(self, player, value):
        self._active[player] = value

    def clear_active(self):
        for player in range(4):
            self.set_active(player, False)

    def play_area(self, player):
        return self._play_area[player]

    def set_play_area(self, player, action):
        self._play_area[player] = action
        self.set_active(player, True)

    def set_my_play_area(self, action):
        assert self.my_id() != -1
        self.set_play_area(self.my_id(), action)

    def record_cards(self, action):
        for card in action['action']:
            rank = card[1]
            if rank == 'JOKER':
                if card[0] == 0:
                    rank = 'JOKER_0'
                else:
                    rank = 'JOKER_1'
            if rank not in utils.card_ranks:
                continue
            if rank not in self._cards.keys():
                self._cards[rank] = 0
            else:
                self._cards[rank] += 1
        self._max_rank['Single'] = self._cur_max_rank('Single')
        self._max_rank['Pair'] = self._cur_max_rank('Pair')

    def _get_left_cards_num(self, rank):
        assert rank in utils.card_ranks
        if rank == 'JOKER_0' or rank == 'JOKER_1':
            if rank in self._cards.keys():
                return 2 - self._cards[rank]
            return 2
        if rank in self._cards.keys():
            return 8 - self._cards[rank]
        return 8

    def _cur_max_rank(self, type):
        for rank in reversed(utils.card_ranks):
            if type == 'Single':
                if self._get_left_cards_num(rank) >= 1:
                    return rank
            elif type == 'Pair':
                if self._get_left_cards_num(rank) >= 2:
                    return rank
            else:
                raise AssertionError('Should not reach here')
        return None

    def query_has_larger(self, action):
        pass


class Env:

    def __init__(self):
        self._state = EnvState.PREPARE
        self._mem = PersistentMem()

    def see(self, content):
        if content['type'] not in [0, 1, 2, 5, 6]:
            raise ValueError('Invalid content type: {}'.format(content))

        self._parse(content)
        self._transfer_state()
        self._memoize()

    def my_choice(self, action):
        # Only memoize during normal playing
        if self._state != EnvState.NORMAL_PLAY:
            return

        self._mem.set_my_play_area(action)
        self._mem.record_cards(action)
        self._mem.clear_active()

    def _parse(self, content):
        self._content = content  # Used for debug info
        self.type = content['type']
        if self.type == 0:
            self.winners = content['winners']
        else:
            self.hand_cards = content['hand_cards']
            self.public = content['public']
            self.current_rank = content['current_rank']
            self.current_player = content['current_player']
            self.action_list = content['action_list']
            self.action_performed = content['action_performed']

    def _transfer_state(self):
        assert self.type in [0, 1, 2, 5, 6]

        if self._state == EnvState.PREPARE:
            assert self.type != 0
            if self._see_tribute_or_back():
                self._state = EnvState.TRIBUTE_OR_BACK
            elif self._see_normal_play():
                self._mem.clear_active()
                self._state = EnvState.NORMAL_PLAY
            else:
                raise AssertionError('Should not reach here')
        elif self._state == EnvState.TRIBUTE_OR_BACK:
            assert self.type != 0
            if self._see_normal_play():
                self._state = EnvState.NORMAL_PLAY
        elif self._state == EnvState.NORMAL_PLAY:
            assert self.type in [0, 1, 2]
            if self.type == 0:
                self._mem.refresh()
                self._state = EnvState.PREPARE
            else:
                assert self._see_normal_play()
        else:
            raise AssertionError('Should not reach here')

    def _see_tribute_or_back(self):
        if self.type == 1:
            return self.action_performed['type'] in ['tribute', 'back', 'anti']
        return self.type in [5, 6]

    def _see_normal_play(self):
        if self.type == 1:
            return self.action_performed['type'] not in ['tribute', 'back', 'anti']
        return self.type == 2

    def _memoize(self):
        # Only memoize during normal playing
        if self._state != EnvState.NORMAL_PLAY:
            return

        if self.type == 1:
            self._mem.set_play_area(self.current_player, self.action_performed)
            self._mem.record_cards(self.action_performed)
        elif self.type == 2:
            self._mem.set_my_id(self.current_player)
        else:
            raise AssertionError('Should not reach here')

    def print_play_area(self):
        for player in range(4):
            prefix = '*' if player == self.current_player else ' '
            play_area = self._mem.play_area(player)
            print('{} {}({}): {}'.format(
                prefix, player, self.rest_hand_cards(player),
                utils.action_to_str(play_area)))

    def my_id(self):
        return self._mem.my_id()

    def my_ally(self):
        return utils.ally_player(self._mem.my_id())

    def my_next_player(self):
        return utils.next_player(self._mem.my_id())

    def my_prev_player(self):
        return utils.next_player(self._mem.my_id())

    def rest_hand_cards(self, player):
        return self.public[player]['rest']

    def play_area(self, player):
        return self._mem.play_area(player)

    def is_active(self, player):
        return self._mem.is_active(player)

    def i_have_priority(self):
        assert self.my_id() == self.current_player
        player = utils.prev_player(self.my_id())
        while player != self.current_player:
            if self.is_active(player) and \
                    self.play_area(player)['type'] != 'PASS':
                return False
            player = utils.prev_player(player)
        return True

    def last_card_type(self):
        player = utils.prev_player(self.current_player)
        while player != self.current_player:
            if self.is_active(player):
                action = self.play_area(player)
                if action['type'] != 'PASS':
                    return action['type']
            player = utils.prev_player(player)
        return None

    def last_card_rank(self):
        player = utils.prev_player(self.current_player)
        while player != self.current_player:
            if self.is_active(player):
                action = self.play_area(player)
                if action['type'] != 'PASS':
                    return action['rank']
            player = utils.prev_player(player)
        return None

    def max_rank(self, type):
        assert type == 'Single' or type == 'Pair'
        return self._mem._max_rank[type]
