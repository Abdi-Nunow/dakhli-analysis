import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="Falanqaynta Dakhliga Maalinlaha", layout="centered")

# Background light gray
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
    }
    .stApp {
        background-color: #f5f5f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Falanqaynta Dakhliga Maalinlaha ee Itoobiya")

uploaded_file = st.file_uploader("Ku shub faylka CSV ee dakhliga (ikhtiyaari)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.subheader("Gali xogta si toos ah:")
    with st.form("data_form"):
        date_today = st.date_input("Taariikhda", value=date.today())
        taxpayer_name = st.text_input("Magaca Canshuur Bixiyaha")
        revenue_today = st.number_input("Dakhliga maanta (ETB)", min_value=0.0)
        outstanding = st.number_input("Lacagta aan weli la bixin (ETB)", min_value=0.0)
        tin_number = st.text_input("TIN Number")
        tax_type = st.selectbox(
            "Nooca Canshuurta",
            ["VAT", "TOT", "INCOME TAX", "PROFIT TAX", "LAND TAX", "PROPERTY TAX", "EXERCISE TAX", "OTHER TAX"]
        )
        submitted = st.form_submit_button("Ku dar xogta")

    if submitted:
        df = pd.DataFrame([{
            "Taariikh": date_today,
            "Magaca Canshuur Bixiyaha": taxpayer_name,
            "Dakhli": revenue_today,
            "Lacagta La Leeyahay": outstanding,
            "TIN Number": tin_number,
            "Nooca Canshuurta": tax_type
        }])
    else:
        df = pd.DataFrame()

if not df.empty:
    st.subheader("📈 Natiijooyinka Falanqaynta")
    st.write(df)

    total_revenue = df["Dakhli"].sum()
    total_outstanding = df["Lacagta La Leeyahay"].sum()

    col1, col2 = st.columns(2)
    col1.metric("💰 Wadarta Dakhli", f"{total_revenue:,.2f} ETB")
    col2.metric("📌 Lacagta La Leeyahay", f"{total_outstanding:,.2f} ETB")

    st.subheader("📊 Dakhli Maalinle ah (Jaantus)")
    fig = px.bar(df, x="Taariikh", y="Dakhli", color="Nooca Canshuurta", title="Dakhli Maalinlaha ee Ku Saleysan Nooca Canshuurta")
    st.plotly_chart(fig)
else:
    st.info("Fadlan gali xog ama ku shub CSV si aad u aragto natiijooyinka.")
