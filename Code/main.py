from simulation import Simulation
from config import PLAYER_COUNT, PAYOFFS

if __name__ == "__main__":
    simulation = Simulation(PLAYER_COUNT, PAYOFFS)
    simulation.run_simulation()
    simulation.plot_population()
