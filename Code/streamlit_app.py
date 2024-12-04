import streamlit as st
from simulation import Simulation
from strategy import Strategy, ALLC, ALLD, TFT, TTT
import matplotlib.pyplot as plt

# Streamlit Sidebar
st.sidebar.header("Simulation Settings")

# Add available strategies
strategy_classes = {"ALLC": ALLC, "ALLD": ALLD, "TFT": TFT, "TTT": TTT}
selected_strategies = st.sidebar.multiselect(
    "Select Strategies", options=list(strategy_classes.keys()), default=list(strategy_classes.keys())
)

# Player Count
player_count = st.sidebar.number_input("Number of Players", min_value=10, max_value=500, value=120, step=10)

# Total Rounds
total_rounds = st.sidebar.number_input("Number of Rounds", min_value=1, max_value=100, value=20)

# Game Rounds
game_rounds = st.sidebar.number_input("Number of Games per Pair", min_value=1, max_value=500, value=100)

# Payoff Matrix
st.sidebar.write("Payoff Matrix")
payoff_CC = st.sidebar.slider("Payoff (C, C)", 0, 10, 3)
payoff_CD = st.sidebar.slider("Payoff (C, D)", 0, 10, 0)
payoff_DC = st.sidebar.slider("Payoff (D, C)", 0, 10, 5)
payoff_DD = st.sidebar.slider("Payoff (D, D)", 0, 10, 1)

payoffs = {
    ("C", "C"): (payoff_CC, payoff_CC),
    ("C", "D"): (payoff_CD, payoff_DC),
    ("D", "C"): (payoff_DC, payoff_CD),
    ("D", "D"): (payoff_DD, payoff_DD),
}

# Initial Strategy Distribution
st.sidebar.write("Initial Strategy Distribution")
initial_distribution = {}
for strategy in selected_strategies:
    initial_distribution[strategy] = st.sidebar.number_input(
        f"{strategy} Players", min_value=0, max_value=player_count, value=player_count // len(selected_strategies)
    )

# Ensure total players match
remaining_players = player_count - sum(initial_distribution.values())
if remaining_players > 0:
    st.sidebar.warning(f"{remaining_players} players unassigned. Adjust the distribution.")

# Run Simulation
if st.sidebar.button("Run Simulation"):
    st.write("### Simulation Results")
    
    # Initialize simulation with selected strategies
    sim = Simulation(player_count, payoffs, selected_strategies, total_rounds, game_rounds)
    
    # Set initial distribution
    sim.initialize_players(initial_distribution)
    
    # Run simulation
    sim.run_simulation()
    
    # Plot results
    fig, ax = plt.subplots()
    for strategy_name, populations in sim.strategy_population.items():
        if strategy_name in selected_strategies:  # Ensure only selected strategies are plotted
            ax.plot(populations, label=strategy_name)
    ax.set_xlabel("Round")
    ax.set_ylabel("Population")
    ax.set_title("Strategy Population Over Time")
    ax.legend()
    st.pyplot(fig)
