import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
# 👉 Custom background color (light gray)
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

st.set_page_config(page_title="Falanqaynta Dakhliga Maalinlaha", layout="centered")

st.title("📊 Falanqaynta Dakhliga Maalinlaha ee Itoobiya")

st.markdown("App-kan wuxuu kuu oggolaanayaa inaad geliso xogta dakhli maalinle ah, \
fahanto inta macmiil ee la adeegsaday, lacagaha la helay, iyo kuwa wali la sugayo. \
Waxa kale oo lagu dari karaa TIN No iyo nooca canshuurta.")

# ------------------------------
# 📥 Geli xog cusub (form)
# ------------------------------

st.header("➕ Geli Xog Cusub")

with st.form("form_dakhli"):
    taariikh = st.date_input("Taariikhda", value=date.today())
    magaca_macmiilka = st.text_input("Magaca Macmiilka")
    dakhli = st.number_input("Dakhliga La Qabtay (ETB)", min_value=0.0, format="%.2f")
    lacag_bixisay = st.number_input("Lacagtii La Bixiyay (ETB)", min_value=0.0, format="%.2f")
    
    # ✅ TIN Number
    tin_no = st.text_input("TIN Number (Lambarka Canshuurta)")

    # ✅ Nooca Canshuurta
    nooca_canshuurta = st.selectbox("Nooca Canshuurta", [
        "VAT", "TOT", "INCOME TAX", "PROFIT TAX",
        "LAND TAX", "PROPERTY TAX", "EXERCISE TAX", "OTHER TAX"
    ])

    submit = st.form_submit_button("💾 Kaydi")

# ------------------------------
# ✅ Marka la kaydiyo xogta
# ------------------------------

if submit:
    xog_cusub = pd.DataFrame([{
        "Taariikh": taariikh,
        "Magac": magaca_macmiilka,
        "Dakhli": dakhli,
        "Lacag Bixisay": lacag_bixisay,
        "Lacag La Sugayo": dakhli - lacag_bixisay,
        "TIN No": tin_no,
        "Nooca Canshuurta": nooca_canshuurta
    }])

    try:
        xog_hore = pd.read_csv("xog_dakhli.csv")
        xog_dhamaystiran = pd.concat([xog_hore, xog_cusub], ignore_index=True)
    except FileNotFoundError:
        xog_dhamaystiran = xog_cusub

    xog_dhamaystiran.to_csv("xog_dakhli.csv", index=False)
    st.success("✅ Xogta waa la keydiyay!")

# ------------------------------
# 📊 Akhri oo soo bandhig xogta
# ------------------------------

st.header("📁 Xogta Maalinlaha ah")

try:
    df = pd.read_csv("xog_dakhli.csv")
    st.dataframe(df)

    # Tiro guud
    st.subheader("📌 Warbixin Kooban")
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Macaamiil", len(df))
    col2.metric("💰 Wadarta Dakhli", f"{df['Dakhli'].sum():,.2f} ETB")
    col3.metric("❗ Lacag La Sugayo", f"{df['Lacag La Sugayo'].sum():,.2f} ETB")

    # Garaafka dakhli taariikhda
    st.subheader("📈 Dakhli Maalinle ah")
    fig = px.bar(df, x="Taariikh", y="Dakhli", color="Nooca Canshuurta",
                 title="Dakhli Maalinle ah oo loo kala qaaday nooca canshuurta")
    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.warning("Ma jiro fayl xog hore ah. Marka hore geli xog si aad u aragto warbixin.")

