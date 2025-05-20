import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Somali Region structure
somali_region = {
    "Afder Zone": ["Bare", "Elekere", "GodGod", "Hargelle", "Mirab Imi", "Ilig Dheere", "Raaso", "Qooxle", "Doollo bay", "Baarey", "washaaqo", "ciid laami", "xagar moqor"],
    "Dhawa Zone": ["Hudet", "Lahey", "Mubaarak", "Qadhaadhumo", "malka mari", "Ceel Goof", "Ceel orba", "Dheer dheertu", "Ceel dheer"],
    "Dollo Zone": ["Boh", "Danot", "Daratole", "Geladin", "Gal-Hamur", "Lehel-Yucub", "Warder", "Yamarugley", "Urmadag"],
    "Erer Zone": ["Fiq", "Lagahida", "Mayaa-muluqo", "Qubi", "Salahad", "Waangaay", "Xamaro", "Yaxoob"],
    "Fafan Zone": ["Awbare", "Babille", "Goljano", "Gursum", "Harawo", "Haroorays", "Harshin", "Jijiga", "Kebri Beyah", "Qooraan", "Shabeeley", "Wajale", "Tuli Guled"],
    "Jarar Zone": ["Araarso", "Awaare", "Bilcil buur", "Birqod", "Daroor", "Degehabur"],
    "Dhagaxmadow": ["Dig", "Gunagado", "Misraq Gashamo", "Yoocaale"],
    "Korahe Zone": ["Boodaley", "Ceel-Ogadeen", "Dobawein", "Higloley", "Kebri Dahar", "Kudunbuur", "Laas-dhankayre", "Marsin", "Shekosh", "Shilavo"],
    "Liben Zone": ["Bokolmayo", "Deka Softi", "Dollo Ado", "Filtu", "Kersa Dula", "Gooro bakaksa", "Gurra damole"],
    "Nogob Zone": ["Ayun", "Duhun", "Elweyne", "Gerbo", "Hararey", "Hora-shagax", "Segeg"],
    "Shabelle Zone": ["Abaaqoorow", "Adadle", "Beercaano", "Danan", "Elele", "Ferfer", "Gode"],
    "Sitti Zone": ["Adigala", "Afdem", "Ayesha", "Bike", "Dambal", "Erer", "Gablalu", "Mieso", "Shinile", "Dhunyar", "Daymeed"]
}

kable_list = [f"Kable {str(i).zfill(2)}" for i in range(1, 41)]
tax_types = ["VAT", "TOT", "INCOME TAX", "PROFIT TAX", "LAND TAX", "PROPERTY TAX", "EXERCISE TAX", "OTHER TAX"]
years = list(range(1990, datetime.now().year + 1))

st.set_page_config(page_title="Dakhli Analysis App", layout="wide")
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Dakhli Analysis Tool")

st.sidebar.header("Ku qor macluumaadka")
name = st.sidebar.text_input("Magaca Canshur Bixiyaha")
tin = st.sidebar.text_input("TIN Number")
mobile = st.sidebar.text_input("Mobile Number")
zone = st.sidebar.selectbox("Deegaanka (Zone)", list(somali_region.keys()))
district = st.sidebar.selectbox("Degmada (District)", somali_region[zone])
kable = st.sidebar.selectbox("Kable", kable_list)
tax_type = st.sidebar.selectbox("Nooca Canshuurta", tax_types)
year = st.sidebar.selectbox("Sanadka Canshuurta", years[::-1])
date = st.sidebar.date_input("Taariikhda Maanta", datetime.today())
income = st.sidebar.number_input("Dakhli Maanta (ETB)", min_value=0.0, step=10.0)
paid = st.sidebar.number_input("Lacag la Bixiyay (ETB)", min_value=0.0, step=10.0)

if st.sidebar.button("💾 Kaydi"):
    new_data = pd.DataFrame({
        "Name": [name],
        "TIN": [tin],
        "Mobile": [mobile],
        "Zone": [zone],
        "District": [district],
        "Kable": [kable],
        "Tax Type": [tax_type],
        "Year": [year],
        "Date": [date],
        "Income": [income],
        "Paid": [paid],
        "Remaining": [income - paid]
    })
    try:
        existing = pd.read_csv("data.csv")
        df = pd.concat([existing, new_data], ignore_index=True)
    except:
        df = new_data
    df.to_csv("data.csv", index=False)
    st.success("Xogta waa la keydiyay 🎉")

# Falanqeyn
st.subheader("Falanqeyn Dakhliga")
try:
    df = pd.read_csv("data.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    st.metric("Tirada Canshur Bixiyeyaasha Maanta", df[df["Date"] == datetime.today().date()].shape[0])
    st.metric("Dakhliga Maanta", f"ETB {df[df['Date'] == datetime.today().date()]['Income'].sum():,.2f}")
    st.metric("Lacagta la Bixiyay Maanta", f"ETB {df[df['Date'] == datetime.today().date()]['Paid'].sum():,.2f}")
    st.metric("Lacagta La Hayo Maanta", f"ETB {df[df['Date'] == datetime.today().date()]['Remaining'].sum():,.2f}")

    fig = px.bar(df, x="Zone", y="Income", color="Tax Type", title="Dakhliga Gobolka")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df)

except FileNotFoundError:
    st.warning("Xog lama helin. Fadlan geli xog si aad u aragto falanqeyn.")
