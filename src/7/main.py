from enum import Enum
from collections import Counter
from functools import total_ordering


@total_ordering
class HandType(Enum):
    FiveOfAKind = 7
    FourOfAKind = 6
    FullHouse = 5
    ThreeOfAKind = 4
    TwoPair = 3
    OnePair = 2
    HighCard = 1

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class Hand:
    SUITS_ORDER = {
        "A": 13,
        "K": 12,
        "Q": 11,
        "J": 10,
        "T": 9,
        "9": 8,
        "8": 7,
        "7": 6,
        "6": 5,
        "5": 4,
        "4": 3,
        "3": 2,
        "2": 1,
    }
    SUITS_ORDER_JOCKER = {
        "A": 13,
        "K": 12,
        "Q": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
        "J": 1,
    }

    JOCKER = "J"


    def contains_jocker(self):
        return Hand.JOCKER in self.hand


    def parse_without_jocker(self, hand):

        hist = Counter(hand).most_common()
        if hist[0][1] == 5:
            return HandType.FiveOfAKind
        if hist[0][1] == 4:
            return HandType.FourOfAKind
        if hist[0][1] == 3 and hist[1][1] == 2:
            return HandType.FullHouse
        if hist[0][1] == 3 and hist[1][1] == 1:
            return HandType.ThreeOfAKind
        if hist[0][1] == 2 and hist[1][1] == 2:
            return HandType.TwoPair
        if hist[0][1] == 2 and hist[1][1] == 1:
            return HandType.OnePair
        else:
            return HandType.HighCard

    def parse(self, hand):
        if self.with_jocker and self.contains_jocker:
            hist = Counter(self.hand).most_common()
            if hist[0][0] == Hand.JOCKER and hist[0][1] < 5:
                hand = hand.replace(hist[1][0], Hand.JOCKER)
            else:
                hand = hand.replace(Hand.JOCKER, hist[0][0])
        return self.parse_without_jocker(hand)

    def __init__(self, hand, bid, with_jocker):
        self.bid = int(bid)
        self.hand = hand
        self.with_jocker = with_jocker
        self.type = self.parse(hand)

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            suits_order = (
                Hand.SUITS_ORDER_JOCKER if self.with_jocker else Hand.SUITS_ORDER
            )
            if self.type == other.type:
                for i in range(5):
                    if suits_order[self.hand[i]] == suits_order[other.hand[i]]:
                        continue
                    else:
                        return suits_order[self.hand[i]] < suits_order[other.hand[i]]
            else:
                return self.type < other.type

        return NotImplemented


def solve(with_jocker=False):
    hands = [
        Hand(hand, bid, with_jocker)
        for (hand, bid) in list(map(lambda x: x.split(), lines))
    ]
    hands.sort()
    total = 0
    for i, hand in enumerate(hands):
        total += (i + 1) * hand.bid
    return total


with open("input.txt", "r", encoding="UTF8") as f:
    lines = f.read().splitlines()

print(f"Part 1: {solve(False)}")
print(f"Part 2: {solve(True)}")
