import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Cybersecurity Analytics", layout="wide")

st.title("Cybersecurity Threat Analysis Dashboard (2015-2024)")

# cargar dataset
data_path = os.path.join("data", "cybersecurity.csv")
df = pd.read_csv(data_path)

# ===== SIDEBAR FILTROS =====
st.sidebar.header("Filters")

country_filter = st.sidebar.multiselect(
    "Select Country",
    options=df["country"].unique(),
    default=df["country"].unique()
)

industry_filter = st.sidebar.multiselect(
    "Select Industry",
    options=df["industry"].unique(),
    default=df["industry"].unique()
)

year_filter = st.sidebar.multiselect(
    "Select Year",
    options=df["year"].unique(),
    default=df["year"].unique()
)

filtered_df = df[
    (df["country"].isin(country_filter)) &
    (df["industry"].isin(industry_filter)) &
    (df["year"].isin(year_filter))
]

# ===== METRICAS =====
total_attacks = filtered_df.shape[0]
total_loss = filtered_df["financial_loss"].sum()
total_users = filtered_df["affected_users"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Cyber Attacks", total_attacks)
col2.metric("Total Financial Loss ($)", f"${total_loss:,}")
col3.metric("Affected Users", f"{total_users:,}")

st.divider()

# ===== GRAFICO ATAQUES POR AÑO =====
st.subheader("Cyber Attacks by Year")

attacks_year = filtered_df.groupby("year").size().reset_index(name="attacks")

fig1 = px.line(
    attacks_year,
    x="year",
    y="attacks",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

# ===== INDUSTRIAS =====
st.subheader("Most Targeted Industries")

industry = filtered_df["industry"].value_counts().reset_index()
industry.columns = ["industry", "attacks"]

fig2 = px.bar(
    industry,
    x="industry",
    y="attacks"
)

st.plotly_chart(fig2, use_container_width=True)

# ===== PAISES =====
st.subheader("Attacks by Country")

countries = filtered_df["country"].value_counts().reset_index()
countries.columns = ["country", "attacks"]

fig3 = px.bar(
    countries,
    x="country",
    y="attacks"
)

st.plotly_chart(fig3, use_container_width=True)

# ===== PERDIDAS =====
st.subheader("Financial Loss by Attack Type")

loss = filtered_df.groupby("attack_type")["financial_loss"].sum().reset_index()

fig4 = px.pie(
    loss,
    values="financial_loss",
    names="attack_type"
)

st.plotly_chart(fig4, use_container_width=True)

# ===== TABLA FINAL =====
st.subheader("Filtered Dataset")

st.dataframe(filtered_df)
