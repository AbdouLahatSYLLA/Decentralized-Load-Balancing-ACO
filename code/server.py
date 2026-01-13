import random

class Server:
    def __init__(self, server_id, capacity):
        self.id = server_id
        self.capacity = capacity  # Requêtes traitées par unité de temps
        self.load = 0             # Nombre de requêtes en cours
        self.is_active = True
        self.pheromone = 1.0      # Valeur initiale (pour ACO)

    def get_response_time(self):
        """Simule un temps de réponse (Loi de Little simplifiée)."""
        if not self.is_active:
            return float('inf')
        # Plus la charge est haute par rapport à la capacité, plus c'est lent
        base_delay = 1.0 / self.capacity
        queuing_delay = self.load * 0.1
        return base_delay + queuing_delay + random.uniform(0.01, 0.05)