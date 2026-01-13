import numpy as np
import matplotlib.pyplot as plt
import random

# --- CONFIGURATION ---
NUM_SERVERS = 3
SIMULATION_STEPS = 1000
REQUEST_PROBABILITY = 0.7  # Probabilité qu'une requête arrive à chaque tick
EVAPORATION_RATE = 0.05  # Taux d'évaporation par tick
BASE_PHEROMONE = 10.0  # Niveau initial
MIN_PHEROMONE = 0.1  # Seuil minimal pour éviter la division par zéro
FAILURE_TIME = 400  # Moment où le serveur 1 tombe en panne (Scenario Robustesse)


# --- CLASSES DU MODÈLE ---

class Server:
    def __init__(self, id, processing_speed=1):
        self.id = id
        self.processing_speed = processing_speed  # Requêtes traitées par tick
        self.queue = []  # File d'attente des requêtes (temps restants)
        self.pheromone = BASE_PHEROMONE
        self.is_active = True
        self.total_processed = 0

    def tick(self):
        # 1. Évaporation constante (Règle locale: Feedback Négatif)
        self.pheromone *= (1 - EVAPORATION_RATE)
        if self.pheromone < MIN_PHEROMONE:
            self.pheromone = MIN_PHEROMONE

        # 2. Traitement des requêtes
        if self.is_active and self.queue:
            # On réduit le temps restant de la requête en tête
            self.queue[0] -= self.processing_speed
            if self.queue[0] <= 0:
                self.queue.pop(0)  # Requête terminée
                self.total_processed += 1
                # 3. Dépôt de phéromone (Règle locale: Feedback Positif)
                # Plus la file était vide, plus c'était rapide, plus on dépose.
                # Formule simplifiée : Récompense l'absence de file d'attente
                reward = 5.0 / (len(self.queue) + 1)
                self.pheromone += reward

    def add_request(self, duration):
        if self.is_active:
            self.queue.append(duration)
            return True
        return False

    def get_load(self):
        return len(self.queue)


# --- ALGORYTHMES DE LOAD BALANCING ---

def get_server_round_robin(servers, current_index):
    # Approche centralisée déterministe
    available = [s for s in servers if s.is_active]
    if not available: return None, current_index
    server = available[current_index % len(available)]
    return server, (current_index + 1)


def get_server_aco(servers):
    # Approche décentralisée probabiliste
    active_servers = [s for s in servers if s.is_active]
    if not active_servers: return None

    # Calcul des probabilités basé sur les phéromones
    total_pheromone = sum(s.pheromone for s in active_servers)
    probabilities = [s.pheromone / total_pheromone for s in active_servers]

    # Sélection "Roulette Wheel"
    chosen_server = np.random.choice(active_servers, p=probabilities)
    return chosen_server


# --- MOTEUR DE SIMULATION ---

def run_simulation(mode="ACO"):
    servers = [Server(i) for i in range(NUM_SERVERS)]
    # Metrics containers
    loads_over_time = {i: [] for i in range(NUM_SERVERS)}
    response_times = []

    rr_index = 0  # Pour Round Robin uniquement

    print(f"--- Démarrage Simulation : {mode} ---")

    for t in range(SIMULATION_STEPS):
        # SCENARIO : Panne du Serveur 1 à t=200
        if t == FAILURE_TIME:
            print(f"[!] Temps {t}: Panne du Serveur 1")
            servers[1].is_active = False
            servers[1].pheromone = 0  # La piste disparaît
            servers[1].queue = []  # Les requêtes sont perdues ou redirigées (ici perdues pour simplifier)


        if t == FAILURE_TIME+500:
            print(f"[!] Temps {t}: Panne du Serveur 4")
            servers[3].is_active = False
            servers[3].pheromone = 0  # La piste disparaît
            servers[3].queue = []  # Les requêtes sont perdues ou redirigées (ici perdues pour simplifier)

        # 1. Mise à jour des serveurs (Processing + Phéromones)
        for s in servers:
            s.tick()
            loads_over_time[s.id].append(s.get_load())

        # 2. Arrivée d'une nouvelle requête (Probabiliste)
        if random.random() < REQUEST_PROBABILITY:
            req_duration = random.randint(3, 8)  # Durée de traitement aléatoire

            if mode == "ACO":
                chosen_server = get_server_aco(servers)
            else:
                chosen_server, rr_index = get_server_round_robin(servers, rr_index)

            if chosen_server:
                chosen_server.add_request(req_duration)

    return loads_over_time, servers


# --- EXÉCUTION & VISUALISATION ---

# 1. Lancer ACO
aco_loads, aco_servers = run_simulation("ACO")
# 2. Lancer Round Robin (Baseline)
rr_loads, rr_servers = run_simulation("Round Robin")

# 3. Graphiques
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

# Plot ACO
for s_id, load in aco_loads.items():
    ax1.plot(load, label=f'Serveur {s_id}')
ax1.axvline(x=FAILURE_TIME, color='r', linestyle='--', label='Panne Serveur 1')
ax1.set_title('ACO: Charge des serveurs (Auto-organisation)')
ax1.set_ylabel('Requêtes en attente')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot Round Robin
for s_id, load in rr_loads.items():
    ax2.plot(load, label=f'Serveur {s_id}')
ax2.axvline(x=FAILURE_TIME, color='r', linestyle='--', label='Panne Serveur 1')
ax2.set_title('Round Robin: Charge des serveurs (Centralisé)')
ax2.set_ylabel('Requêtes en attente')
ax2.set_xlabel('Temps (ticks)')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Stats finales
print("\n--- RÉSULTATS FINAUX ---")
print(f"ACO - Total traité: {sum(s.total_processed for s in aco_servers)}")
print(f"RR  - Total traité: {sum(s.total_processed for s in rr_servers)}")