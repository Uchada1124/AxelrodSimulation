from typing import List, Tuple
from strategy import Strategy

class Player:
    def __init__(self, player_id: int, strategy: Strategy) -> None:
        self.id: int = player_id
        self.strategy: Strategy = strategy
        self.score: int = 0
        self.previous_actions: List[Tuple[str, str]] = []

    def choose_action(self) -> str:
        return self.strategy.choose_action(self.previous_actions)

    def update_score(self, points: int) -> None:
        self.score += points
