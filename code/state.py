import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la base
DB_CONFIG = {
    'host': '92.158.18.97',
    'port': '5432',
    'dbname': 'lol',
    'user': 'postgres',
    'password': 'root'  # ← à remplacer
}

# Ordre des mois en français
MOIS_FR = [
    "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre",
    "Octobre", "Novembre", "Décembre", "Janvier", "Février", "Mars"
]

# Dictionnaire de traduction mois anglais → français
TRAD_MOIS = {
    "January": "Janvier", "February": "Février", "March": "Mars",
    "April": "Avril", "May": "Mai", "June": "Juin",
    "July": "Juillet", "August": "Août", "September": "Septembre",
    "October": "Octobre", "November": "Novembre", "December": "Décembre"
}

def charger_donnees():
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql("SELECT * FROM stats_champ;", conn)
    conn.close()

    # Traduction des mois en français
    df["month_name"] = df["month_name"].map(TRAD_MOIS)
    df["mois_ordre"] = df["month_name"].apply(lambda x: MOIS_FR.index(x) if x in MOIS_FR else -1)
    df["mois_periode"] = df["period_name"] + " - " + df["month_name"]
    return df

def statistiques(df):
    print("📊 Statistiques globales :")
    print(f"Pickrate moyen : {df['pickrate'].mean():.2f}%")
    print(f"Winrate moyen : {df['winrate'].mean():.2f}%")
    print(f"Banrate moyen : {df['banrate'].mean():.2f}%\n")

def graphe_pickrate_mensuel_barres(df):
    df_barres = (
        df.groupby(["period_name", "month_name", "mois_ordre"])
        .agg({"pickrate": "mean"})
        .reset_index()
        .sort_values(["mois_ordre", "period_name"])
    )

    df_barres["month_name"] = pd.Categorical(df_barres["month_name"], categories=MOIS_FR, ordered=True)

    plt.figure(figsize=(14, 6))
    sns.barplot(
        data=df_barres,
        x="month_name",
        y="pickrate",
        hue="period_name",
        palette="Set2"
    )
    plt.title("📈 Pickrate moyen par mois (par période)")
    plt.xlabel("Mois")
    plt.ylabel("Pickrate moyen (%)")
    plt.legend(title="Période")
    plt.tight_layout()
    plt.show()

def graphe_top_champions(df):
    top10 = df.groupby("champion_name")["pickrate"].mean().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 5))
    sns.barplot(y=top10.index, x=top10.values, palette="viridis")
    plt.title("🏆 Top 10 champions les plus pickés (moyenne)")
    plt.xlabel("Pickrate moyen (%)")
    plt.ylabel("Champion")
    plt.tight_layout()
    plt.show()

def graphe_correlation_moyenne(df):
    df_avg = df.groupby("champion_name")[["pickrate", "winrate"]].mean().reset_index()

    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=df_avg,
        x="pickrate",
        y="winrate",
        hue="winrate",
        size="pickrate",
        palette="coolwarm",
        sizes=(30, 200),
        legend=False,
        alpha=0.8
    )
    sns.regplot(
        data=df_avg,
        x="pickrate",
        y="winrate",
        scatter=False,
        color="black",
        line_kws={"linestyle": "dashed"}
    )
    plt.title("📊 Corrélation Pickrate / Winrate (moyenne par champion)")
    plt.xlabel("Pickrate moyen (%)")
    plt.ylabel("Winrate moyen (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    df = charger_donnees()
    statistiques(df)
    graphe_pickrate_mensuel_barres(df)
    graphe_top_champions(df)
    graphe_correlation_moyenne(df)

if __name__ == "__main__":
    main()
