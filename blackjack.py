import sys
import random

from typing import List, Dict, Tuple

def make_deck(N: int) -> Dict[str, int]:
    # NOTE (Henrique): [spades, diamonds, clubs, hearts]
    SUITS = ["♠", "♦", "♣", "♥"]
    CARDS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    deck = []
    for suit in SUITS:
        for card in CARDS:
           deck.append(card + suit)

    LEN_DECK = 52
    assert len(deck) == LEN_DECK

    deck *= N
    return deck

def give_hand(deck: List[str], size: int) -> List[int]:
    N = len(deck)
    hand_indices = random.sample(range(N), size)
    return [deck[index] for index in hand_indices]

def is_ace_in_hand(hand: List[str]) -> bool:
    return any(["A" in x for x in hand])

def eval_hand(hand: List[str]) -> int: 
    value_table_A = {"A":  1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}

    hand_value = 0 
    for card in hand: 
        value = card[0]
        hand_value += value_table_A[value]
    
    if hand_value < 12 and is_ace_in_hand(hand):
        hand_value += 10

    return hand_value 

def main(argv: List[str]) -> int: 

    random.seed(2)

    deck = make_deck(2)
    hand = give_hand(deck, 2)

    hand = ["A♦", "J♣", "3♦"]
    print(hand)
    vb = eval_hand(hand)
    print(vb)

    return 0

if __name__ == "__main__":
    main(sys.argv)