from typing import Dict, Tuple
from player import Player

class Game:
    def __init__(self, player1: Player, player2: Player, payoffs: Dict[Tuple[str, str], Tuple[int, int]], rounds: int = 100) -> None:
        self.player1: Player = player1
        self.player2: Player = player2
        self.payoffs: Dict[Tuple[str, str], Tuple[int, int]] = payoffs
        self.rounds: int = rounds

    def play(self) -> None:
        for _ in range(self.rounds):
            action1 = self.player1.choose_action()
            action2 = self.player2.choose_action()
            payoff1, payoff2 = self.payoffs[(action1, action2)]

            self.player1.update_score(payoff1)
            self.player2.update_score(payoff2)

            self.player1.previous_actions.append((action1, action2))
            self.player2.previous_actions.append((action2, action1))
