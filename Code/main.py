import itertools
import random
from collections import Counter

class Player:
    def __init__(self, player_id, strategy_type):
        self.player_id = player_id
        self.strategy_type = strategy_type

class Game:
    def __init__(self, actions, strategies, payoffs):
        self.actions = actions
        self.strategies = strategies
        self.payoffs = payoffs

def get_strategies(actions):
    n = len(actions)
    all_combinations = itertools.product(range(2), repeat=n)

    strategies = []
    for combination in all_combinations:
        strategy = [actions[i] for i in combination]
        strategies.append(strategy)
    
    return strategies

def get_player_pairs(player_n):
    if player_n % 2 != 0:
        raise ValueError("The number of players must be even to form pairs.")
    
    players = list(range(1, player_n + 1))
    random.shuffle(players)
    player_pairs = [(players[i], players[i + 1]) for i in range(0, player_n, 2)]
    
    return player_pairs

def assign_strategy_types(player_n, strategy_type, probability_simplex=None):
    if probability_simplex == None:
        probability_simplex = [player_n//len(strategy_type) for i in strategy_type]

    strategy_assignment_list = []
    for i in range(len(probability_simplex)):
        for j in range(probability_simplex[i]):
            strategy_assignment_list.append(strategy_type[i])

    random.shuffle(strategy_assignment_list)

    strategy_assignment_dict = {(i + 1): strategy_assignment_list[i] for i in range(0, len(strategy_assignment_list))}

    return strategy_assignment_dict

def main():
    actions = ['C', 'D']
    strategies = [
        ('C', 'C'),
        ('C', 'D'),
        ('D', 'C'),
        ('D', 'D'),
        ]
    payoffs = {
        ('C', 'C'): (3, 3),
        ('C', 'D'): (0, 5),
        ('D', 'C'): (5, 0),
        ('D', 'D'): (1, 1)
    }

    player_n = 120
    strategy_type = {
        0: 'ALLC',
        1: 'ALLD',
        2: 'TFT'
    }

    player_pairs = get_player_pairs(player_n)
    print(f"Player Pairs ({len(player_pairs)} pairs):")
    print(player_pairs)

    strategy_assignment = assign_strategy_types(player_n, strategy_type)
    print("\nStrategy Assignments:")
    print(strategy_assignment)
    strategy_counts = Counter(strategy_assignment.values())
    for strategy, count in strategy_counts.items():
        print(f"{strategy}: {count}")

if __name__ == '__main__':
    main()
