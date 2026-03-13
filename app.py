import streamlit as st


st.set_page_config(page_title="App ML Multi-Pages", layout="wide")

st.title("🚀 Application ML Multi-Pages")

st.markdown(
    """
### Navigation
Utilisez le menu de gauche pour accéder aux différentes pages :

- **Data** : Upload et exploration des données
- **Training** : Entraînement du modèle et performances
- **Prediction** : Interface de prédiction sur de nouvelles données
"""
)

st.info(
    "Sélectionnez une page dans la barre latérale « Pages » (générée automatiquement par Streamlit)."
)

