from typing import Dict, Tuple, List
from game import Game
from player import Player
from strategy import Strategy
import random
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

class Simulation:
    def __init__(self, player_count: int, payoffs: Dict[Tuple[str, str], Tuple[int, int]], total_rounds: int = 20, game_rounds: int = 100) -> None:
        self.player_count: int = player_count
        self.payoffs: Dict[Tuple[str, str], Tuple[int, int]] = payoffs
        self.total_rounds: int = total_rounds
        self.game_rounds: int = game_rounds
        self.players: List[Player] = []
        self.strategy_population: Dict[str, List[int]] = defaultdict(list)

    def initialize_players(self, initial_distribution: Dict[str, int]) -> None:
        self.players = []
        for strategy_name, count in initial_distribution.items():
            strategy_class = Strategy.registry[strategy_name]
            for _ in range(count):
                player_id = len(self.players) + 1
                self.players.append(Player(player_id, strategy_class()))

    def generate_pairs(self) -> List[Tuple[Player, Player]]:
        random.shuffle(self.players)
        return [(self.players[i], self.players[i + 1]) for i in range(0, len(self.players), 2)]

    def update_strategy_population(self) -> None:
        strategy_counts = Counter(player.strategy.name for player in self.players)
        for strategy_name in Strategy.registry.keys():
            self.strategy_population[strategy_name].append(strategy_counts[strategy_name])

    def update_player_strategies(self) -> None:
        scores_by_strategy = Counter()
        for player in self.players:
            scores_by_strategy[player.strategy.name] += player.score

        total_scores = sum(scores_by_strategy.values())
        new_distribution = {
            strategy_name: int((scores_by_strategy[strategy_name] / total_scores) * self.player_count)
            for strategy_name in Strategy.registry.keys()
        }

        total_assigned = sum(new_distribution.values())
        surplus = self.player_count - total_assigned
        if surplus > 0:
            sorted_strategies = sorted(
                Strategy.registry.keys(),
                key=lambda name: scores_by_strategy[name],
                reverse=True
            )
            for strategy_name in sorted_strategies:
                if surplus == 0:
                    break
                new_distribution[strategy_name] += 1
                surplus -= 1

        self.initialize_players(new_distribution)

    def run_round(self) -> None:
        pairs = self.generate_pairs()
        for player1, player2 in pairs:
            game = Game(player1, player2, self.payoffs, self.game_rounds)
            game.play()
        self.update_strategy_population()
        self.update_player_strategies()

    def run_simulation(self) -> None:
        initial_distribution = {
            strategy_name: self.player_count // len(Strategy.registry)
            for strategy_name in Strategy.registry.keys()
        }
        surplus = self.player_count - sum(initial_distribution.values())
        strategies = list(initial_distribution.keys())
        for _ in range(surplus):
            initial_distribution[random.choice(strategies)] += 1

        self.initialize_players(initial_distribution)

        for _ in range(self.total_rounds):
            self.run_round()

    def plot_population(self) -> None:
        for strategy_name, populations in self.strategy_population.items():
            plt.plot(populations, label=strategy_name)
        plt.legend()
        plt.xlabel('Round')
        plt.ylabel('Population')
        plt.title('Strategy Population Over Time')
        plt.show()