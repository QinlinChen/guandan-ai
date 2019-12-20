
def prev_player(player):
    return (player + 3) % 4


def next_player(player):
    return (player + 1) % 4


def ally_player(player):
    return (player + 2) % 4


def rank_order(rank):
    map = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
        '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14,
        'JOKER': 15, 'PASS': 0
    }
    return map[rank]


def card_type_order(card_type):
    map = {
        'Single': 0, 'Pair': 1, 'Trips': 1,
        'ThreePair': 3, 'TripsPair': 3, 'ThreeWithTwo': 5,
        'Straight': 6, 'StraightFlush': 7, 'Bomb': 8,
        'PASS': 9, 'tribute': 9, 'back': 9
    }
    return map[card_type]


def suit_to_str(suit):
    map = ['♠', '♥', '♣', '♦']
    return map[suit]


def card_to_str(card):
    if card[1] == 'PASS':
        return 'PASS'
    if card[1] == 'JOKER':
        return '{}{}'.format(card[0], card[1])
    return '{}{}'.format(suit_to_str(card[0]), card[1])


def cards_to_str(cards):
    return ','.join([card_to_str(card) for card in cards])


def action_to_str(action):
    return '({}) {}'.format(action['type'], cards_to_str(action['action']))


card_types = [
    'Single', 'Pair', 'Trips', 'ThreePair', 'ThreeWithTwo', 'TripsPair',
    'Straight', 'StraightFlush', 'Bomb', 'JOKER'
]


def is_fire_card(card_type):
    return card_type in ['StraightFlush', 'Bomb', 'JOKER']


def hand_cards_count(hand_cards):
    count = dict()
    for hand_card in hand_cards:
        rank = hand_card[1]
        _attr_init_and_append(count, rank, hand_card)
    return count


def partition(hand_cards):
    counter = hand_cards_count(hand_cards)
    result = dict()

    bucket = dict([(size, []) for size in range(1, 9)])
    ordered_rank = list(counter.keys())
    ordered_rank.sort(key=rank_order)
    for rank in ordered_rank:
        cards = counter[rank]
        if rank == 'JOKER' and len(cards) >= 2:
            _attr_init_and_append(result, 'JOKER', cards)
        else:
            bucket[len(cards)].append(cards)

    for single in bucket[1]:
        _attr_init_and_append(result, 'Single', single)

    for trips in bucket[3]:
        if len(bucket[2]) > 0:
            pair = bucket[2].pop(0)
            _attr_init_and_append(result, 'ThreeWithTwo', trips + pair)
        else:
            _attr_init_and_append(result, 'Trips', trips)

    for pair in bucket[2]:
        _attr_init_and_append(result, 'Pair', pair)

    for size in range(4, 9):
        for bomb in bucket[size]:
            _attr_init_and_append(result, 'Bomb', bomb)

    return result


def _attr_init_and_append(obj, attr, val):
    if attr not in obj:
        obj[attr] = []
    obj[attr].append(val)


if __name__ == "__main__":

    hand_cards = [[0, '2'], [1, '2'], [0, '2'], [0, '3'], [3, '4'],
                  [1, '4'], [0, '7'], [3, '10'], [0, '10'], [3, 'J'],
                  [0, 'K'], [3, 'A'], [3, '5'], [0, '5'], [0, 'JOKER']]

    partition(hand_cards)
