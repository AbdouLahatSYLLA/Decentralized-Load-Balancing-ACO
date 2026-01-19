# Decentralized Load Balancing using Ant Colony Optimization (ACO)

This repository contains a **Self-Organizing System (SOS)** simulation that implements a decentralized load balancer inspired by the foraging behavior of ant colonies.

## Overview

Traditional load balancers (like Nginx or HAProxy) typically rely on a centralized controller, which creates a **Single Point of Failure (SPOF)** and potential bottlenecks. This project demonstrates an alternative where global load equilibrium emerges from local interactions between requests ("ants") and servers ("food sources").

## The SOS Model

The system is governed by the mathematical principles of **Ant Colony Optimization (ACO)**:

* **Pheromone Deposit (Positive Feedback):** When a server processes a request quickly, it increases its "pheromone" score. The deposit is calculated as .


* 
**Pheromone Evaporation (Negative Feedback):** Pheromones decay over time (), allowing the system to "forget" outdated performance data and adapt to changes like server failures.


* 
**Stochastic Selection:** Requests choose servers based on a probability  that balances past performance () and current real-time load ().



## Key Features

* 
**Decentralized Logic:** No single node has a global view of the system.


* 
**Self-Healing:** The system automatically detects and bypasses failed servers through pheromone evaporation.


* 
**Anti-Stagnation:** Integrated heuristic weights () to prevent "Winner-Take-All" effects where one server monopolizes all traffic.



## Project Structure

```text
├── simulation.py        # Core SimPy orchestration
├── server.py            # Server entity with dynamic response times
├── request.py           # Request (Ant) entity
├── load_balancer.py     # ACO and Round Robin selection logic
├── experiments.py       # Scenarios (Baseline vs. Robustness test)
├── plots.py             # Matplotlib/Seaborn visualization suite
└── results/             # Generated performance graphs

```

## Running the Simulation

1. **Install dependencies:**
```bash
pip install simpy pandas matplotlib seaborn numpy

```


2. **Execute experiments:**
```bash
python experiments.py

```


This will run two simulations (ACO vs. Round Robin) and inject a server failure at .



## Results

### Pheromone Evolution

The system achieves a stable oscillating equilibrium where all servers share the load. When a failure occurs, the failed node's pheromone drops to the minimum threshold instantly.

### Load Distribution

The distribution heatmap confirms that the "intelligence" of the colony successfully redistributes tasks to healthy nodes in real-time without manual reconfiguration.

## Academic Context

* 
**Module:** Self-Organizing Systems (2025-2026) 


* 
**Institution:** University POLITEHNICA of Bucharest 


* 
**Professor:** Mrs. Stefania Alexandra 


* 
**Author:** Abdou Lahat SYLLA 
