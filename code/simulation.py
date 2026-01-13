import simpy
from server import Server
from load_balancer import LoadBalancer
from request import Request


def request_process(env, req, lb, mode, stats, evaporation_rate):
    # Sélection du serveur selon le mode
    server = lb.select_aco() if mode == "ACO" else lb.select_round_robin()

    if server:
        server.load += 1
        req.assigned_server_id = server.id

        duration = server.get_response_time()
        yield env.timeout(duration)

        req.completion_time = env.now
        server.load -= 1

        # Mise à jour ACO si nécessaire
        if mode == "ACO":
            lb.update_pheromones(server, req.response_time())

        stats.append(req)


def evaporation_process(env, servers, rate=0.5): # Augmenté à 0.5 selon le cours
    """Global pheromone evaporation process[cite: 104, 256]."""
    while True:
        yield env.timeout(1.0)
        for s in servers:
            # Formula: tau = (1 - rho) * tau [cite: 105, 265]
            s.pheromone *= (1 - rate)
            # Maintain a minimum to allow re-discovery [cite: 529, 748]
            s.pheromone = max(s.pheromone, 0.1)