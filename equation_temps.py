import numpy as np
import matplotlib.pyplot as plt
import datetime

def equation_du_temps(jour):
    # Conversion du jour en angle (en radians)
    B = 2 * np.pi * (jour - 81) / 364  
    # Approximation de l'équation du temps (en minutes)
    EOT = -(9.87 * np.sin(2 * B) - 7.53 * np.cos(B) - 1.5 * np.sin(B))
    return EOT

def create_eot_plot(annee):
    # Générer les valeurs pour l'année entière
    jours = np.arange(1, 366)
    eot_values = [equation_du_temps(j) for j in jours]

    # Création des étiquettes des mois
    mois_labels = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"]
    mois_positions = [15, 46, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349]

    # Calcul des points remarquables
    day_max = np.argmax(eot_values) + 1
    day_min = np.argmin(eot_values) + 1
    max_value = max(eot_values)
    min_value = min(eot_values)

    # Points d'inflexion
    inflection_days = [j for j in range(1, 364) if (eot_values[j-1] - eot_values[j]) * (eot_values[j] - eot_values[j+1]) < 0]
    inflection_values = [eot_values[j] for j in inflection_days]

    # Passages à zéro
    zero_crossings = [j for j in range(1, 365) if eot_values[j-1] * eot_values[j] < 0]
    zero_values = [eot_values[j] for j in zero_crossings]

    # Conversion des dates
    inflection_dates = [datetime.datetime(annee, 1, 1) + datetime.timedelta(days=j-1) for j in inflection_days]
    inflection_labels = [f"{date.day} {mois_labels[date.month-1]}" for date in inflection_dates]

    zero_dates = [datetime.datetime(annee, 1, 1) + datetime.timedelta(days=j-1) for j in zero_crossings]
    zero_labels = [f"{date.day} {mois_labels[date.month-1]}" for date in zero_dates]

    # Création du graphique
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(jours, eot_values, label="Équation du temps", color='r')
    ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
    ax.set_xticks(mois_positions)
    ax.set_xticklabels(mois_labels)
    ax.set_xlabel("Mois de l'année")
    ax.set_ylabel("Équation du temps (minutes)")
    ax.set_title(f"Équation du Temps - Année {annee}")
    ax.legend()
    ax.grid(True)

    # Points remarquables
    ax.scatter([day_max, day_min], [max_value, min_value], color='blue', zorder=3)
    ax.text(day_max, max_value, f"Max: {max_value:.1f} min", fontsize=10, 
            verticalalignment='bottom', horizontalalignment='right', color='blue', fontweight='bold')
    ax.text(day_min, min_value, f"Min: {min_value:.1f} min", fontsize=10, 
            verticalalignment='top', horizontalalignment='right', color='blue', fontweight='bold')

    # Points d'inflexion
    ax.scatter(inflection_days, inflection_values, color='green', zorder=3)
    for i in range(len(inflection_days)):
        ax.text(inflection_days[i], inflection_values[i] + 0.5, 
                f"{inflection_labels[i]}\n{inflection_values[i]:.1f} min", 
                fontsize=9, verticalalignment='bottom', horizontalalignment='center', 
                color='green', fontweight='bold')

    # Passages à zéro
    ax.scatter(zero_crossings, zero_values, color='red', zorder=3)
    for i in range(len(zero_crossings)):
        ax.text(zero_crossings[i], 0.5, f"{zero_labels[i]}", fontsize=10, 
                verticalalignment='bottom', horizontalalignment='center', 
                color='red', fontweight='bold')

    plt.tight_layout()
    return fig