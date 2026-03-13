import streamlit as st

# -------- LOGIN -------- #
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Application Streamlit démarrée")
def login():

    st.title("🔐 Authentification")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Se connecter"):

        if username == "test" and password == "test":
            st.session_state["logged_in"] = True
        else:
            st.error("Identifiants incorrects")


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


if not st.session_state["logged_in"]:
    login()
    st.stop()


# -------- APPLICATION -------- #

st.set_page_config(page_title="App ML Multi-Pages", layout="wide")

st.set_page_config(
    page_title="App ML Multi-Pages",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("🚀 Application ML Multi-Pages")

st.markdown("""
Utilisez le menu de gauche pour accéder aux pages :

- Data
- Training
- Prediction

""")
