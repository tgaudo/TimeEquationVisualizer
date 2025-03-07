import streamlit as st
import datetime
from equation_temps import create_eot_plot
from io import BytesIO

# Configuration de la page
st.set_page_config(
    page_title="Équation du Temps",
    page_icon="⌚",
    layout="wide"
)

# Titre et introduction
st.title("📊 Visualisation de l'Équation du Temps")

st.markdown("""
Cette application permet de visualiser l'équation du temps, qui décrit la différence entre le temps solaire moyen 
et le temps solaire vrai au cours d'une année.

### Qu'est-ce que l'équation du temps ?
L'équation du temps est la différence entre le temps solaire moyen (celui de nos montres) et le temps solaire vrai 
(celui indiqué par un cadran solaire). Cette différence varie au cours de l'année en raison de deux facteurs principaux :
- L'inclinaison de l'axe de rotation de la Terre
- L'excentricité de l'orbite terrestre

### Formule de l'équation du temps
L'équation du temps (EdT) est calculée selon la formule suivante :

$$ EdT = 4 * (AD - LM) $$

Où :
- EdT est exprimée en minutes
- AD (Ascension Droite) = $\\arctan(\\cos(\\varepsilon) \\cdot \\sin(L), \\cos(L))$
- LM (Longitude Moyenne) = $280.460 + 0.9856474 \\cdot T$
- L (Longitude vraie) = $LM + 1.915 \\cdot \\sin(M) + 0.020 \\cdot \\sin(2M)$
- M (Anomalie Moyenne) = $357.528 + 0.9856003 \\cdot T$
- T est le nombre de jours depuis le 1er janvier 2000 à 12h TU
- $\\varepsilon$ est l'obliquité de l'écliptique (23.439281°)
""")

# Sélection de l'année
annee = st.number_input("Sélectionnez l'année", 
                       min_value=1900, 
                       max_value=2100, 
                       value=datetime.datetime.now().year,
                       step=1)

# Création et affichage du graphique
st.markdown("### Graphique de l'équation du temps")
fig = create_eot_plot(annee)
st.pyplot(fig)

# Explications des points remarquables
st.markdown("""
### Points remarquables sur le graphique

- **Points rouges** : Passages à zéro (moments où le temps solaire moyen égale le temps solaire vrai)
- **Points bleus** : Valeurs maximales et minimales de l'équation
- **Points verts** : Points d'inflexion (changements de direction de la courbe)

### Utilisation pratique
Ce graphique est particulièrement utile pour :
- Régler les cadrans solaires
- Comprendre les variations saisonnières du midi solaire
- Étudier les phénomènes astronomiques liés au mouvement apparent du Soleil
""")

# Convertir la figure en bytes pour le téléchargement
buf = BytesIO()
fig.savefig(buf, format='png')
buf.seek(0)
btn = st.download_button(
    label="📥 Télécharger le graphique",
    data=buf,
    file_name=f"equation_temps_{annee}.png",
    mime="image/png"
)

# Footer
st.markdown("---")
st.markdown("*Application développée avec Streamlit, Matplotlib et NumPy*")