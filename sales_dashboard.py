import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


st.set_page_config(page_title="Dashboard de Ventes", page_icon="📊", layout="wide")

st.title("📊 Dashboard Interactif de Ventes")


@st.cache_data
def generate_sales_data():
    mois = pd.date_range("2024-01-01", periods=12, freq="MS")
    categories = ["Électronique", "Vêtements", "Maison", "Sport"]
    regions = ["Nord", "Sud", "Est", "Ouest"]

    data = []
    np.random.seed(42)
    for m in mois:
        for cat in categories:
            for reg in regions:
                ventes = np.random.randint(1000, 10000)
                data.append(
                    {
                        "Mois": m,
                        "Mois_str": m.strftime("%b"),
                        "Catégorie": cat,
                        "Région": reg,
                        "Ventes": ventes,
                    }
                )
    df = pd.DataFrame(data)
    return df


df = generate_sales_data()

st.sidebar.title("Filtres")
month_options = df["Mois"].dt.strftime("%Y-%m").unique().tolist()
selected_months = st.sidebar.multiselect(
    "Période (mois)",
    options=month_options,
    default=month_options,
)
cat_options = df["Catégorie"].unique().tolist()
selected_cats = st.sidebar.multiselect(
    "Catégories",
    options=cat_options,
    default=cat_options,
)

mask = (
    df["Mois"].dt.strftime("%Y-%m").isin(selected_months)
    & df["Catégorie"].isin(selected_cats)
)
filtered_df = df[mask]

st.sidebar.markdown("---")
st.sidebar.info(f"{len(filtered_df)} lignes après filtrage")

tab1, tab2, tab3, tab4 = st.tabs(
    ["📄 Données", "📈 Graphiques", "📊 Statistiques", "🗺 Carte"]
)

with tab1:
    st.subheader("Tableau de données")
    mois_str_options = filtered_df["Mois_str"].unique().tolist()
    mois_choisi = st.multiselect(
        "Filtrer par mois (affichage)",
        options=mois_str_options,
        default=mois_str_options,
    )

    df_table = filtered_df[filtered_df["Mois_str"].isin(mois_choisi)]
    st.dataframe(df_table, use_container_width=True)

with tab2:
    st.subheader("Évolution temporelle et par catégorie")

    df_time = (
        filtered_df.groupby("Mois", as_index=False)["Ventes"].sum().sort_values("Mois")
    )
    fig_line = px.line(
        df_time,
        x="Mois",
        y="Ventes",
        markers=True,
        title="Ventes totales par mois",
    )
    st.plotly_chart(fig_line, use_container_width=True)

    df_cat = (
        filtered_df.groupby("Catégorie", as_index=False)["Ventes"].sum().sort_values(
            "Ventes", ascending=False
        )
    )
    fig_bar = px.bar(
        df_cat,
        x="Catégorie",
        y="Ventes",
        title="Ventes par catégorie",
        color="Catégorie",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.subheader("Statistiques globales")

    total = filtered_df["Ventes"].sum()
    mean = filtered_df["Ventes"].mean()
    vmax = filtered_df["Ventes"].max()
    vmin = filtered_df["Ventes"].min()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total des ventes", f"{total:,.0f} €")
    c2.metric("Moyenne", f"{mean:,.0f} €")
    c3.metric("Max", f"{vmax:,.0f} €")
    c4.metric("Min", f"{vmin:,.0f} €")

    st.markdown("---")
    st.subheader("Top 10 lignes (par ventes)")
    st.dataframe(
        filtered_df.sort_values("Ventes", ascending=False).head(10),
        use_container_width=True,
    )

with tab4:
    st.subheader("Carte géographique des ventes (régions fictives)")

    region_coords = {
        "Nord": (50.5, 2.5),
        "Sud": (43.5, 5.0),
        "Est": (48.0, 7.8),
        "Ouest": (47.2, -1.6),
    }

    df_map = filtered_df.groupby("Région", as_index=False)["Ventes"].sum().copy()
    df_map["lat"] = df_map["Région"].map(lambda r: region_coords[r][0])
    df_map["lon"] = df_map["Région"].map(lambda r: region_coords[r][1])

    st.map(df_map[["lat", "lon", "Ventes"]])
    st.write("Les positions sont fictives et servent uniquement à illustrer une carte.")

