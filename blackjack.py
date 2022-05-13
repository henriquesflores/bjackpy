import os
import sys
import pdb
import random

from typing import List

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

# NOTE (Henrique): This function alters deck state
def draw_hand(deck: List[str], size: int) -> List[str]:
    hand_indices = random.sample(range(len(deck) - 1), size)
    return [deck.pop(index) for index in hand_indices]

def is_ace_in_hand(hand: List[str]) -> bool:
    return any(["A" in x for x in hand])

def eval_hand(hand: List[str]) -> int: 
    value_map = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
    hand_value = 0 
    for card in hand: 
        value = card[:-1] 
        hand_value += value_map[value]
    
    if hand_value < 12 and is_ace_in_hand(hand):
        hand_value += 10

    return hand_value 

class Game: 
    def __init__(self, players: int, decks: List[str], initial_cash: List[float]):
        self.players = list(range(players))
        self.alive = [True] * players 
        self.deck = decks

        self.hands = [None] * players 
        self.values = [None] * players 
        self.money = [None] * players
        for player in self.players: 
            self.hands[player] = ["x", "x"]
            self.values[player] = 0
            self.money[player] = initial_cash[player] 

    def update_hand_value(self, player: int) -> None:
        self.values[player] = eval_hand(self.hands[player])
        return None
    
    def is_bust(self, player: int) -> bool:
        if self.values[player] > 21:
            self.alive[player] = False
        
        return self.alive[player]

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")
    return None

def render(game: Game) -> None:
    clear_screen()
    print(f"Deck has {len(game.deck)} cards left.\n")
    str_hand = "|" + "| |".join(game.hands[0]) + "|"
    print("\tDealer:\t" + str_hand + f" ({game.values[0]})")
    print("")
    for player in game.players[1:]:
        if game.alive[player]:
            str_hand = "|" + "| |".join(game.hands[player]) + "|"
            print(f"\tPlayer {player}: " + str_hand + f" ({game.values[player]})")
        else:
            str_hand = "|" + "| |".join(game.hands[player]) + "|"
            print("\t(BUST!) " + f"Player {player}: " + str_hand + f" ({game.values[player]})")
    return None 

# NOTE (Henrique): 
# h -> hit
# s -> stop
class UserInput:
    msg = "{player}: H (Hit), S (Stop): "
    map = {"h": draw_hand, "s": lambda *args: None, "q": lambda *args: sys.exit(0)}
    actions = "".join(map.keys())

    @staticmethod
    def prompt_actions(player: int) -> None:
        name = "Dealer" if player == 0 else f"Player {player}"
        print("")
        print(UserInput.msg.format(player = name), end = " ")
        return None

    @staticmethod 
    def get_input(player: int) -> str:
        UserInput.prompt_actions(player)
        while True:
            action = input()[0].lower()
            if action not in UserInput.actions:
                print(f"Unrecognized action!")
            else:
                return action.lower()

def ask_for_bets() -> None:
    size = input()
    return None

def update_and_render(game: Game) -> None:
    # TODO (Henrique): Before first round. There should be a round of bets 
    render(game)
    ask_for_bets()
    for player in game.players:
        game.hands[player] = draw_hand(game.deck, 2)
        game.values[player] = eval_hand(game.hands[player])
        if len(game.deck) < 2:
            print("Deck is empty.")
            break

    # TODO (Henrique): Need to check if player is bust and remove from subsequent rounds
    # TODO (Henrique): Command messages to exit
    player = 1
    while True:
        render(game)
        action = UserInput.get_input(player) 
        maybe_card = UserInput.map[action](game.deck, 1)
        if maybe_card is not None: 
            card = maybe_card[0]
            game.hands[player].append(card)
            game.update_hand_value(player)
        else:
            player += 1
            if player > (len(game.players) - 1): break

    while True:
        render(game)
        action = UserInput.get_input(0) 
        maybe_card = UserInput.map[action](game.deck, 1)
        if maybe_card is not None: 
            card = maybe_card[0]
            game.hands[0].append(card)
            game.update_hand_value(0)
        else:
            break

def main(argv: List[str]) -> int: 
    
    random.seed(2)
    cashs = [10.3, 4.8, 2.1]
    game = Game(players = 3, decks = make_deck(1), initial_cash = cashs)
    update_and_render(game)

    return 0

if __name__ == "__main__":
    main(sys.argv)