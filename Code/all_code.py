import random
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Type

class Strategy:
    registry: Dict[str, Type['Strategy']] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Strategy.registry[cls.__name__] = cls

    def __init__(self, name: str) -> None:
        self.name: str = name

    def choose_action(self, previous_actions: List[Tuple[str, str]]) -> str:
        raise NotImplementedError("This method should be implemented by subclasses")

class ALLC(Strategy):
    def __init__(self) -> None:
        super().__init__("ALLC")

    def choose_action(self, previous_actions: List[Tuple[str, str]]) -> str:
        return 'C'

class ALLD(Strategy):
    def __init__(self) -> None:
        super().__init__("ALLD")

    def choose_action(self, previous_actions: List[Tuple[str, str]]) -> str:
        return 'D'

class TFT(Strategy):
    def __init__(self) -> None:
        super().__init__("TFT")

    def choose_action(self, previous_actions: List[Tuple[str, str]]) -> str:
        if not previous_actions:
            return 'C'
        return previous_actions[-1][1]

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

if __name__ == "__main__":
    player_count = 120
    payoffs = {
        ('C', 'C'): (3, 3),
        ('C', 'D'): (0, 5),
        ('D', 'C'): (5, 0),
        ('D', 'D'): (1, 1)
    }
    simulation = Simulation(player_count, payoffs)
    simulation.run_simulation()
    simulation.plot_population()
