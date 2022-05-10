import sys
import random

from typing import List, Dict

# NOTE (Henrique): [spades, diamonds, clubs, hearts]
SUITS = ["♠", "♦", "♣", "♥"]
#CARDS = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13} 
CARDS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
LEN_DECK = 52

def make_deck() -> Dict[str, int]:
    deck = []
    for suit in SUITS:
        for card in CARDS:
           deck.append(card + suit)

    return deck

def shuffle(N_decks: int) -> List[int]:
    return random.sample(range(52), 4 * N_decks)

def main(argv: List[str]) -> int: 

    random.seed(42)

    deck = make_deck()
    order = shuffle(1)
    hand = [deck[card] for card in order]
    print(hand)

    return 0

if __name__ == "__main__":
    main(sys.argv)