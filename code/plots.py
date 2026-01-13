import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Configuration esthétique
plt.style.use('seaborn-v0_8-muted')
sns.set_context("paper", font_scale=1.2)


def plot_performance_comparison(aco_stats, rr_stats, save_path='results/'):
    """Compare le temps de réponse moyen entre ACO et Round Robin."""
    if not os.path.exists(save_path): os.makedirs(save_path)

    # Préparation des données
    df_aco = pd.DataFrame([vars(s) for s in aco_stats])
    df_aco['Method'] = 'ACO'
    df_rr = pd.DataFrame([vars(s) for s in rr_stats])
    df_rr['Method'] = 'Round Robin'

    combined_df = pd.concat([df_aco, df_rr])
    combined_df['resp_time'] = combined_df['completion_time'] - combined_df['arrival_time']

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=combined_df, x='arrival_time', y='resp_time', hue='Method')
    plt.title("Temps de réponse : ACO vs Round Robin")
    plt.xlabel("Temps de simulation (s)")
    plt.ylabel("Temps de réponse (s)")
    plt.grid(True, linestyle='--')
    plt.savefig(f"{save_path}comparison_plot.png")
    plt.close()


def plot_server_load(aco_stats, n_servers, save_path='results/'):
    """Affiche la distribution des requêtes par serveur (Heatmap de charge)."""
    df = pd.DataFrame([vars(s) for s in aco_stats])
    df['count'] = 1

    # Grouper par fenêtres de temps pour voir l'évolution
    df['time_bin'] = (df['arrival_time'] // 10) * 10
    pivot_table = df.pivot_table(index='assigned_server_id', columns='time_bin', values='count', aggfunc='sum').fillna(
        0)

    plt.figure(figsize=(12, 5))
    sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", fmt='g')
    plt.title("Distribution de la charge par serveur (ACO)")
    plt.xlabel("Temps de simulation (s)")
    plt.ylabel("ID du Serveur")
    plt.savefig(f"{save_path}load_distribution.png")
    plt.close()


def plot_pheromone_evolution(pheromone_logs, save_path='results/'):
    """Affiche l'évolution des phéromones (idéal pour montrer la résilience)."""
    plt.figure(figsize=(10, 6))
    for server_id, history in pheromone_logs.items():
        times = [h[0] for h in history]
        levels = [h[1] for h in history]
        plt.plot(times, levels, label=f"Serveur {server_id}")

    plt.title("Évolution des Phéromones (Adaptabilité & Robustesse)")
    plt.xlabel("Temps (s)")
    plt.ylabel("Niveau de Phéromone")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{save_path}pheromone_evolution.png")
    plt.close()