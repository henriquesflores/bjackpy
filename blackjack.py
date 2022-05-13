import os
import sys
import pdb
import random
from tkinter import W

from typing import List, Union, Callable, Any

from scipy.fftpack import shift

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

def shift_list(lst: List[Any]) -> List[Any]:
    x = lst[1:].copy() 
    x.append(lst[0])
    return x

class Game: 
    def __init__(self, players: int, decks: List[str]):
        self.players = list(range(players))
        self.ordered_players = shift_list(self.players)
        self.alive = [True] * players 
        self.deck = decks

        self.bets = [None] * players
        self.money = [None] * players
        self.hands = [None] * players 
        self.values = [None] * players 
        for player in self.players: 
            self.hands[player] = ["x", "x"]
            self.values[player] = 0
            self.money[player] = 0 
            self.bets[player] = 0

    def update_player(self, player: int, card: str) -> None:
        self.hands[player].append(card)
        self.values[player] = eval_hand(self.hands[player])
        return None

    def check_player_status(self, player: int) -> None:
        if self.values[player] > 21:
            self.alive[player] = False

    def next_available_player(self, player: int) -> int:
        # TODO (Henrique): There is a bug in this function
        pdb.set_trace()
        next_player = self.ordered_players[player]
        if self.alive[next_player]:
            return next_player
        else: 
            return None
        

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")
    return None

def render(game: Game) -> None:
    # TODO (Henrique): Think about how to render bet and amount
    clear_screen()
    print(f"Deck has {len(game.deck)} cards left.\n")
    str_hand = "|" + "| |".join(game.hands[0]) + "|"
    print("\tDealer:\t" + str_hand + f" ({game.values[0]})")
    print("")
    for player in game.players[1:]:
        if game.alive[player]:
            str_hand = "|" + "| |".join(game.hands[player]) + "|"
            print(f"\tPlayer {player} ({game.bets[player]}/{game.money[player]}): " + str_hand + f" ({game.values[player]})")
        else:
            str_hand = "|" + "| |".join(game.hands[player]) + "|"
            print("\t(BUST!) " + f"Player {player}: " + str_hand + f" ({game.values[player]})")
    return None 

def validate_bet(value: int, actions: List[int]) -> Union[int, None]:
    if any(map(lambda x: value == x, actions)):
        return value
    return None

class UserInput:
    cash_msg = "Player {player}, enter initial cash: "
    
    hit_msg = "{player} -- H (Hit), S (Stop): "
    hit_map = {"h": draw_hand, "s": lambda *args: None, "q": lambda *args: sys.exit(0)}
    hit_actions = "".join(hit_map.keys())
    
    bet_msg = "\nPlayer {player}, Bet (0, 5c, 10c, 20c): "
    bet_actions = [0, 5, 10, 20]

    @staticmethod
    def get_initial_cash(player: int) -> float:
        while True:
            value = input(UserInput.cash_msg.format(player = player))
            if value.isnumeric():
                return float(value)
            else:
                print("Unrecognized initial cash amount!")
       
    @staticmethod
    def get_bet(player: int) -> float:
        while True:
            value = input(UserInput.bet_msg.format(player = player))
            if value.isnumeric():
                maybe_value = validate_bet(int(value), UserInput.bet_actions)
                if maybe_value is None:
                    continue
                else:
                    return maybe_value / 100
            else:
                print("Unrecognized bet amount!") 

    @staticmethod
    def prompt_actions(player: int) -> None:
        name = "Dealer" if player == 0 else f"Player {player}"
        print(UserInput.hit_msg.format(player = name), end = " ")
        return None

    @staticmethod 
    def maybe_hit(player: int) -> Callable:
        while True:
            UserInput.prompt_actions(player)
            action = input()[0].lower()
            if action not in UserInput.hit_actions:
                print("Unrecognized action!")
            else:
                return action.lower()

def ask_for_cash(game: Game) -> None:
    for player in game.players[1:]:
        amount = UserInput.get_initial_cash(player)
        game.money[player] = amount
    return None

def ask_for_bets(game: Game) -> None:
    for player in game.players[1:]:
        while True:
            bet_amount = UserInput.get_bet(player)
            if bet_amount > game.money[player]:
                continue
            else:
                game.bets[player] = bet_amount
                game.money[player] -= bet_amount
                if bet_amount == 0:
                    game.alive[player] = False
                break

    return None

def get_first_available_player(game: Game) -> int:
    for index, state in enumerate(game.alive[1:], start = 1):
        if state:
            return index
    
    return 0

def update_and_render(game: Game) -> None:

    clear_screen()
    ask_for_cash(game)
    render(game)

    ask_for_bets(game)
    render(game)
    for player in game.players:
        game.hands[player] = draw_hand(game.deck, 2)
        game.values[player] = eval_hand(game.hands[player])
    render(game) 

    player = get_first_available_player(game) 
    while True:
        action = UserInput.maybe_hit(player)
        maybe_card = UserInput.hit_map[action](game.deck, 1)
        if maybe_card is not None:
            card = maybe_card[0]
            game.update_player(player, card)
            game.check_player_status(player)
            player = game.next_available_player(player)
            render(game)
            if player == -1:
                break
        else: 
            player = game.next_available_player(player)
            if player == -1:
                break

def main(argv: List[str]) -> int: 
    
    random.seed(2)
    game = Game(players = 3, decks = make_deck(1))
    update_and_render(game)

    return 0

if __name__ == "__main__":
    main(sys.argv)