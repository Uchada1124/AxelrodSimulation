from simulation import Simulation
from config import PLAYER_COUNT, PAYOFFS, SELECTED_STRATEGY_TYPES

if __name__ == "__main__":
    simulation = Simulation(PLAYER_COUNT, PAYOFFS, SELECTED_STRATEGY_TYPES)
    simulation.run_simulation()
    simulation.plot_population()
