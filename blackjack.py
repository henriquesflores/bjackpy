import sys
import pdb
import random

from typing import List, Dict, Tuple

def make_deck(N: int) -> List[str]:
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

def give_hand(deck: List[str], size: int) -> List[str]:
    hand_indices = random.sample(range(len(deck) - 1), size)
    return [deck.pop(index) for index in hand_indices]

def is_ace_in_hand(hand: List[str]) -> bool:
    return any(["A" in x for x in hand])

def eval_hand(hand: List[str]) -> int: 
    value_map = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}

    hand_value = 0 
    for card in hand: 
        value = card[0]
        hand_value += value_map[value]
    
    if hand_value < 12 and is_ace_in_hand(hand):
        hand_value += 10

    return hand_value 

def render_game(hands: Dict[int, List[str]], values: List[int]) -> None:
    for (player, hand), value in zip(hands.items(), values):
        str_hand = "|" + "| |".join(hand) + "|"
        if player == 0: 
            print("Dealer:\t" + str_hand + f" ({value})")
            print("")
        else:
            print(f"Player {player}: " + str_hand + f" ({value})")

    return None 

def perform_action(action: str) -> callable:
    if action == "h":
        return give_hand
    elif action == "s":
        return lambda *args: None


# TODO (Henrique): Extract into appropriate structure and handle extra actions
# NOTE (Henrique): 
# h -> hit
# s -> stop
actions = "hs"
def evolve_game(deck: List[str], hands: Dict[int, List[str]], values: List[int]) -> None:
    # TODO (Henrique): Dealer is player zero. Should loop through 1...0
    players = zip(hands.items(), values)
    for (player, hand), hand_value in players:
        # This string should work together with the available actions.
        print(f"Player {player}: Hit (H), Stop (S)")
        action = input()[0]
        if action.lower() not in actions:
            print("Unrecognized action.")
            # TODO (Henrique): Handle better user input. Should goto input again.
            sys.exit(1)
        else: 
            maybe_card = perform_action(action)(deck, 1)
            if maybe_card is None: 
                print("Stop! Next player") 
            else:
                print(*maybe_card) 

def main(argv: List[str]) -> int: 
    
    random.seed(2)
    players = 3
    deck = make_deck(1)

    # TODO (Henrique): Before first round. There should be a round of bets 
    players_hand = {}
    for player in range(players):
        players_hand[player] = give_hand(deck, 2)
        if len(deck) < 2:
            print("Deck is empty.")
    players_values = list(map(eval_hand, players_hand.values()))
    
    # TODO (Henrique): It would be nice to clean render every action performed
    # TODO (Henrique): Game state are hands for every player
#    while True:
    render_game(players_hand, players_values)
#   evolve_game(deck, players_hand, players_values)

    return 0

if __name__ == "__main__":
    main(sys.argv)