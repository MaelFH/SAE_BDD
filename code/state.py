import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data for champions
champions = [
    'Aatrox', 'Ahri', 'Akali', 'Alistar', 'Amumu',
    'Anivia', 'Annie', 'Aphelios', 'Ashe', 'Aurelion Sol',
    'Azir', 'Bard', 'Blitzcrank', 'Brand', 'Braum',
    'Caitlyn', 'Camille', 'Cassiopeia', "Cho'Gath", 'Corki',
    'Darius', 'Diana', 'Draven', 'Ekko', 'Elise',
    'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz',
    'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas',
    'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi',
    'Irelia', 'Ivern', 'Janna', 'Jarvan IV', 'Jax',
    'Jayce', 'Jhin', 'Jinx', "Kai'Sa", 'Kalista'
]

# Data for periods
periods = ['2023-2024', '2024-2025']

# Data for stats: list of tuples with champion_id (1-based), period_id (1-based), pickrate, winrate, banrate
stats_data = [
    # period 1
    (1,1,10.4,51.2,5.8),(2,1,12.1,52.5,7.3),(3,1,11.3,49.7,8.9),(4,1,6.8,50.4,2.1),(5,1,4.9,51.9,3.2),
    (6,1,5.7,53.5,1.8),(7,1,4.8,50.3,1.2),(8,1,7.2,48.9,6.5),(9,1,8.4,49.1,4.1),(10,1,3.5,54.2,5.0),
    (11,1,4.7,48.7,7.7),(12,1,3.6,51.0,1.9),(13,1,9.3,47.8,6.9),(14,1,6.1,49.6,3.4),(15,1,2.8,51.5,2.0),
    (16,1,11.5,48.8,8.0),(17,1,7.9,52.1,5.3),(18,1,5.9,50.9,4.6),(19,1,3.7,50.0,3.0),(20,1,4.2,49.8,2.4),
    (21,1,9.8,49.3,6.5),(22,1,8.6,51.2,5.6),(23,1,7.4,48.5,7.2),(24,1,6.0,51.6,4.1),(25,1,4.5,50.4,3.8),
    (26,1,3.9,52.7,2.5),(27,1,12.9,49.9,4.8),(28,1,2.7,53.6,1.5),(29,1,5.6,50.2,4.4),(30,1,6.4,51.8,5.7),
    (31,1,3.3,48.9,3.6),(32,1,4.0,49.5,3.1),(33,1,8.7,50.7,2.9),(34,1,5.1,51.3,2.7),(35,1,7.0,50.6,4.2),
    (36,1,10.8,49.8,6.1),(37,1,3.2,51.1,2.0),(38,1,6.9,50.8,4.5),(39,1,2.9,52.3,1.4),(40,1,4.4,49.2,3.3),
    (41,1,8.1,50.1,5.2),(42,1,2.5,54.0,1.1),(43,1,4.6,52.8,2.2),(44,1,6.6,50.9,3.7),(45,1,9.2,49.5,6.0),
    (46,1,5.4,48.6,2.8),(47,1,7.7,50.0,4.9),(48,1,11.2,49.8,7.5),(49,1,13.4,51.4,8.3),(50,1,6.3,49.7,4.0),
    # period 2
    (1,2,11.1,52.4,6.4),(2,2,11.8,51.8,7.9),(3,2,10.2,50.1,9.2),(4,2,6.5,50.9,2.0),(5,2,5.1,52.4,3.0),
    (6,2,6.0,54.1,2.3),(7,2,4.2,50.0,1.0),(8,2,7.5,49.4,6.0),(9,2,8.7,49.5,4.3),(10,2,3.9,54.7,5.6),
    (11,2,4.9,49.0,7.2),(12,2,3.4,51.2,2.1),(13,2,8.8,48.4,6.4),(14,2,6.4,50.1,3.1),(15,2,3.1,52.0,2.2),
    (16,2,12.0,49.1,8.4),(17,2,8.3,52.5,5.7),(18,2,6.2,51.3,4.9),(19,2,3.5,50.4,3.4),(20,2,4.6,50.3,2.8),
    (21,2,10.2,49.6,6.8),(22,2,8.9,51.5,5.1),(23,2,7.1,49.0,7.5),(24,2,6.3,51.9,4.4),(25,2,4.8,50.8,4.1),
    (26,2,4.2,53.1,2.7),(27,2,13.2,50.3,5.1),(28,2,2.5,54.0,1.2),(29,2,5.9,50.6,4.6),(30,2,6.1,52.0,5.3),
    (31,2,3.1,49.2,3.4),(32,2,4.3,50.0,3.3),(33,2,9.0,51.0,3.1),(34,2,5.3,51.6,2.5),(35,2,7.3,50.9,4.5),
    (36,2,11.1,50.2,6.4),(37,2,3.5,51.4,2.3),(38,2,7.2,51.1,4.7),(39,2,3.1,52.6,1.6),(40,2,4.7,49.5,3.5),
    (41,2,8.4,50.4,5.5),(42,2,2.8,54.3,1.3),(43,2,4.9,53.1,2.4),(44,2,6.9,51.3,3.9),(45,2,9.5,49.8,6.4),
    (46,2,5.7,48.9,3.0),(47,2,8.0,50.4,5.2),(48,2,11.5,50.1,7.8),(49,2,13.7,51.7,8.5),(50,2,6.6,50.0,4.2)
]

# Create DataFrame from stats_data
df_stats = pd.DataFrame(stats_data, columns=['champion_id', 'period_id', 'pickrate', 'winrate', 'banrate'])

# Add champion and period names
df_stats['champion'] = df_stats['champion_id'].apply(lambda x: champions[x-1])
df_stats['period'] = df_stats['period_id'].apply(lambda x: periods[x-1])

def plot_pickrate(period_name):
    """
    Plot pickrate per champion for the given period.
    """
    df_period = df_stats[df_stats['period'] == period_name]
    df_sorted = df_period.sort_values(by='pickrate', ascending=False)

    plt.figure(figsize=(12, 18))  # Grande hauteur = + d'espacement
    bars = plt.barh(df_sorted['champion'], df_sorted['pickrate'], color='skyblue', height=0.3)
    
    plt.xlabel('Pickrate (%)')
    plt.title(f'Pickrate per Champion for Period {period_name}')
    plt.gca().invert_yaxis()

    # ✅ Espacer les noms et les rendre lisibles
    plt.tick_params(axis='y', labelsize=9)
    plt.subplots_adjust(left=0.3)
    plt.grid(axis='x', linestyle='--', alpha=0.4)

    plt.tight_layout()
    plt.show()


def plot_winrate_comparison():
    """
    Plot winrate comparison for all champions between 2023-2024 and 2024-2025.
    """
    df_pivot = df_stats.pivot(index='champion', columns='period', values='winrate')
    df_pivot = df_pivot.sort_values(by='2024-2025', ascending=False)

    labels = df_pivot.index
    x = np.arange(len(labels))
    width = 0.4

    fig, ax = plt.subplots(figsize=(14, 20))  # Hauteur augmentée
    ax.barh(x - width/2, df_pivot['2023-2024'], height=width, label='2023-2024', color='lightcoral')
    ax.barh(x + width/2, df_pivot['2024-2025'], height=width, label='2024-2025', color='steelblue')

    ax.set_xlabel('Winrate (%)')
    ax.set_title('Winrate Comparison per Champion: 2023–2024 vs 2024–2025')
    ax.set_yticks(x)
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    ax.legend()

    plt.subplots_adjust(left=0.3)
    plt.tight_layout()
    plt.show()


def plot_banrate(period_name):
    """
    Plot banrate per champion for the given period with visual spacing and value labels.
    """
    df_period = df_stats[df_stats['period'] == period_name]
    df_sorted = df_period.sort_values(by='banrate', ascending=False)

    plt.figure(figsize=(12, 18))  # Hauteur suffisante
    bars = plt.barh(df_sorted['champion'], df_sorted['banrate'], color='tomato', edgecolor='black', height=0.3)
    plt.xlabel('Banrate (%)')
    plt.title(f'Banrate per Champion for Period {period_name}')
    plt.gca().invert_yaxis()

    # Espacement et lisibilité
    plt.tick_params(axis='y', labelsize=9)
    plt.subplots_adjust(left=0.3)
    plt.grid(axis='x', linestyle='--', alpha=0.4)

    # Ajouter les valeurs à droite des barres
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.3, bar.get_y() + bar.get_height() / 2,
                 f'{width:.1f}%', va='center', fontsize=9, fontweight='bold', color='black')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Plot pickrate for 2023-2024 as requested by user
    plot_pickrate('2023-2024')
    # Plot pickrate for 2024-2025 as requested by user
    plot_pickrate('2024-2025')
    # Plot winrate comparison for 2023-2024 and 2024-2025 with improved readability
    plot_winrate_comparison()
    # Plot banrate for 2023-2024 with very visual style
    plot_banrate('2023-2024')
    # Plot banrate for 2024-2025 with very visual style
    plot_banrate('2024-2025')