import simpy
import pandas as pd
from simulation import request_process, evaporation_process
from server import Server
from load_balancer import LoadBalancer
from request import Request
import plots


def run_experiment(mode="ACO", sim_time=500, failure_time=200):
    env = simpy.Environment()
    # Identical capacities to test fair load distribution
    servers = [Server(i, capacity=1.0) for i in range(3)]
    lb = LoadBalancer(servers)
    stats = []
    pheromone_logs = {s.id: [] for s in servers}

    def monitor_pheromones(env):
        while True:
            for s in servers:
                pheromone_logs[s.id].append((env.now, s.pheromone))
            yield env.timeout(1)

    def request_gen(env):
        req_id = 0
        while True:
            yield env.timeout(0.5)
            req = Request(req_id, env.now)
            # Use alpha=1.0 and beta=2.0 for balanced exploration [cite: 610, 691]
            env.process(request_process(env, req, lb, mode, stats, evaporation_rate=0.5))
            req_id += 1

    def inject_failure(env):
        if failure_time:
            yield env.timeout(failure_time)
            servers[0].is_active = False  # On coupe le serveur le plus rapide
            print(f"[{env.now}] ALERTE : Panne critique sur Serveur 0")

    # Lancement des processus
    env.process(request_gen(env))
    env.process(evaporation_process(env, servers))
    env.process(monitor_pheromones(env))
    env.process(inject_failure(env))

    env.run(until=sim_time)
    return stats, pheromone_logs


if __name__ == "__main__":
    print("Démarrage des expérimentations...")

    # 1. Test ACO avec panne
    aco_stats, pheromone_logs = run_experiment(mode="ACO", failure_time=200)
    plots.plot_pheromone_evolution(pheromone_logs)
    plots.plot_server_load(aco_stats, 3)

    # 2. Test Round Robin pour comparaison
    rr_stats, _ = run_experiment(mode="RR", failure_time=200)
    plots.plot_performance_comparison(aco_stats, rr_stats)

    print("Expériences terminées. Les graphiques sont dans 'results/'.")