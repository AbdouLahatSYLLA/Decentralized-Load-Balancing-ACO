import numpy as np
import random


class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.rr_index = 0

    def select_round_robin(self):
        """Standard centralized approach."""
        active_servers = [s for s in self.servers if s.is_active]
        if not active_servers: return None
        server = active_servers[self.rr_index % len(active_servers)]
        self.rr_index += 1
        return server

    def select_aco(self, alpha=1.0, beta=2.0):
        """
        Probabilistic selection based on Course 3 formulas.
        alpha: influence of pheromone (collective memory)[cite: 419].
        beta: influence of heuristic (current load)[cite: 420].
        """
        active_servers = [s for s in self.servers if s.is_active]
        if not active_servers: return None

        # Heuristic desirability (eta): 1 / (current load + 1) [cite: 424]
        # This prevents "Winner-Take-All" by making busy servers less attractive.
        etas = np.array([1.0 / (s.load + 1.0) for s in active_servers])
        pheromones = np.array([s.pheromone for s in active_servers])

        # Mathematical formula: P = (tau^alpha * eta^beta) / sum(tau^alpha * eta^beta)
        weights = (pheromones ** alpha) * (etas ** beta)

        total_weight = weights.sum()
        if total_weight == 0:
            probabilities = np.ones(len(active_servers)) / len(active_servers)
        else:
            probabilities = weights / total_weight

        # Stochastic selection (Roulette Wheel) [cite: 463, 464]
        return np.random.choice(active_servers, p=probabilities)

    def update_pheromones(self, server, response_time):
        """
        Pheromone deposit: proportional to quality (1/response_time)[cite: 103, 259].
        """
        deposit = 1.0 / (response_time + 0.001)
        server.pheromone += deposit