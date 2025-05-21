import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io
from docx import Document

st.set_page_config(page_title="Dakhli Analysis App", layout="wide")

# Midabka background-ka
page_bg_color = """
<style>
    .stApp {
        background-color: #f0f0f5;
    }
</style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)

st.title("Falanqaynta Dakhliga Maalinlaha ah ee Canshuuraha")

zones = {
    "Afder": [...],  # Xogta zone-yaasha sidii hore
    "Dhawa": [...],
    "Dollo": [...],
    "Erer": [...],
    "Fafan": [...],
    "Jarar": [...],
    "Korahe": [...],
    "Liben": [...],
    "Nogob": [...],
    "Shabelle": [...],
    "Sitti": [...]
}

kable_list = [f"Kable {i:02}" for i in range(1, 41)]
tax_types = ["VAT", "TOT", "INCOME TAX", "PROFIT TAX", "LAND TAX", "PROPERTY TAX", "EXERCISE TAX", "OTHER TAX"]
years = [str(year) for year in range(1990, datetime.now().year + 1)]

st.header("Geli Xogta Canshuur Bixiyaha")

col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Magaca Canshuur Bixiyaha")
    mobile = st.text_input("Mobile")
    zone = st.selectbox("Gobolka (Zone)", list(zones.keys()))
with col2:
    tin = st.text_input("TIN No (12-digit only)")
    if tin and (not tin.isdigit() or len(tin) != 12):
        st.warning("Fadlan geli TIN sax ah oo ka kooban 12 lambar.")
    district = st.selectbox("Degmada (District)", zones[zone])
    kable = st.selectbox("Kable", kable_list)
with col3:
    tax_type = st.selectbox("Nooca Canshuurta", tax_types)
    tax_year = st.selectbox("Sanadka Canshuurta", years)
    date = st.date_input("Taariikhda", datetime.today(), min_value=datetime(1990, 1, 1))

outstanding_income = st.number_input("Dakhliga Lagu Leeyahay", min_value=0.0, step=0.1)
payment = st.number_input("Lacagta la Bixiyay", min_value=0.0, step=0.1)

if st.button("Kaydi Xogta"):
    if tin and tin.isdigit() and len(tin) == 12:
        data = {
            "Magaca": name,
            "TIN": tin,
            "Mobile": mobile,
            "Zone": zone,
            "District": district,
            "Kable": kable,
            "Tax Type": tax_type,
            "Tax Year": tax_year,
            "Date": date,
            "Income": outstanding_income,
            "Payment": payment,
            "Outstanding": outstanding_income - payment
        }
        df_new = pd.DataFrame([data])

        try:
            df_old = pd.read_csv("dakhli_data.csv")
            df_all = pd.concat([df_old, df_new], ignore_index=True)
        except FileNotFoundError:
            df_all = df_new

        df_all.to_csv("dakhli_data.csv", index=False)
        st.success("Xogta waa la keydiyay ✅")
    else:
        st.error("TIN waa inuu ahaadaa 12 lambar.")

st.header("Falanqaynta Dakhliga")
try:
    df = pd.read_csv("dakhli_data.csv")
    st.dataframe(df)

    today_str = str(datetime.today().date())
    total_clients = df[df['Date'] == today_str].shape[0]
    total_income = df['Income'].sum()
    total_outstanding = df['Outstanding'].sum()

    st.metric("Tirada Canshuur Bixiyayaasha Maanta", total_clients)
    st.metric("Dakhliga Guud", f"{total_income:,.2f}")
    st.metric("Lacagta aan wali la Bixin", f"{total_outstanding:,.2f}")

    fig = px.bar(df, x='Date', y='Income', color='Tax Type', title='Dakhliga Maalinlaha ah')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Soo Degso Xogta")
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine='xlsxwriter')
    st.download_button(
        label="📥 Soo Degso Excel",
        data=excel_buffer.getvalue(),
        file_name="dakhli_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    doc = Document()
    doc.add_heading("Xogta Dakhliga Canshuur Bixiyayaasha", 0)
    table = doc.add_table(rows=1, cols=len(df.columns))
    hdr_cells = table.rows[0].cells
    for i, col in enumerate(df.columns):
        hdr_cells[i].text = col

    for _, row in df.iterrows():
        row_cells = table.add_row().cells
        for i, value in enumerate(row):
            row_cells[i].text = str(value)

    word_buffer = io.BytesIO()
    doc.save(word_buffer)

    st.download_button(
        label="📥 Soo Degso Word",
        data=word_buffer.getvalue(),
        file_name="dakhli_data.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

except FileNotFoundError:
    st.info("Xog lama helin. Fadlan geli xog si aad u aragto falanqayn.")
