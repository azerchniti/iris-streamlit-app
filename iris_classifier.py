import streamlit as st
import pandas as pd
import numpy as np

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


st.set_page_config(page_title="Classification Iris", page_icon="🌸", layout="centered")

st.title("🌸 Classification des Fleurs d'Iris")


@st.cache_data
def load_data():
    iris = load_iris(as_frame=True)
    df = iris.frame
    df.columns = [c.replace(" (cm)", "").replace(" ", "_") for c in df.columns]
    return df, iris.target_names


@st.cache_resource
def train_model(model_type: str = "RandomForest"):
    df, _ = load_data()
    X = df.drop("target", axis=1)
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    if model_type == "LogisticRegression":
        model = LogisticRegression(max_iter=500)
    elif model_type == "SVM (RBF)":
        model = SVC(kernel="rbf", probability=True, gamma="scale", C=1.0)
    elif model_type == "KNN (k=5)":
        model = KNeighborsClassifier(n_neighbors=5)
    elif model_type == "GradientBoosting":
        model = GradientBoostingClassifier(random_state=42)
    else:
        model = RandomForestClassifier(n_estimators=150, random_state=42)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    return model, acc, X.columns.tolist()


df, target_names = load_data()

col_model, col_info = st.columns([2, 1])
with col_model:
    model_type = st.selectbox(
        "Choisissez le modèle",
        [
            "RandomForest",
            "LogisticRegression",
            "SVM (RBF)",
            "KNN (k=5)",
            "GradientBoosting",
        ],
        help="Modèle utilisé pour la classification",
    )
with col_info:
    st.write("**Classes :**")
    for i, name in enumerate(target_names):
        st.write(f"- {i} → {name}")

model, acc, feature_names = train_model(model_type)

st.success(f"Modèle entraîné ({model_type}) – Précision de test : {acc*100:.2f} %")

st.markdown("---")
st.header("Paramètres de la fleur à prédire")

mins = df[feature_names].min()
maxs = df[feature_names].max()
means = df[feature_names].mean()

col1, col2 = st.columns(2)

with col1:
    sepal_length = st.slider(
        "Sepal length (cm)",
        float(mins[feature_names[0]]),
        float(maxs[feature_names[0]]),
        float(means[feature_names[0]]),
        step=0.1,
    )
    sepal_width = st.slider(
        "Sepal width (cm)",
        float(mins[feature_names[1]]),
        float(maxs[feature_names[1]]),
        float(means[feature_names[1]]),
        step=0.1,
    )

with col2:
    petal_length = st.slider(
        "Petal length (cm)",
        float(mins[feature_names[2]]),
        float(maxs[feature_names[2]]),
        float(means[feature_names[2]]),
        step=0.1,
    )
    petal_width = st.slider(
        "Petal width (cm)",
        float(mins[feature_names[3]]),
        float(maxs[feature_names[3]]),
        float(means[feature_names[3]]),
        step=0.1,
    )

input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

if st.button("🌟 Prédire l'espèce", type="primary"):
    pred_class = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0]

    st.markdown("---")
    st.subheader("Résultat de la prédiction")
    st.success(f"Espèce prédite : **{target_names[pred_class]}**")

    prob_df = pd.DataFrame(
        {"Espèce": target_names, "Probabilité": proba}
    ).sort_values("Probabilité", ascending=False)

    st.bar_chart(
        prob_df.set_index("Espèce"),
        height=300,
    )
