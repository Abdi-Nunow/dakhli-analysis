import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

# Hubi inaad horay u rakibtay maktabaddan: pip install python-docx
from docx import Document

# Hubi inaad horay u rakibtay maktabaddan: pip install fpdf
from fpdf import FPDF

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
    "Afder": ["Bare", "Elekere", "GodGod", "Hargelle", "Mirab Imi", "Ilig Dheere", "Raaso", "Qooxle", "Doollo bay", "Baarey", "Washaaqo", "Ciid Laami", "Xagar Moqor"],
    "Dhawa": ["Hudet", "Lahey", "Mubaarak", "Qadhaadhumo", "Malka Mari", "Ceel Goof", "Ceel Orba", "Dheer Dheertu", "Ceel Dheer"],
    "Dollo": ["Boh", "Danot", "Daratole", "Geladin", "Gal-Hamur", "Lehel-Yucub", "Warder", "Yamarugley", "Urmadag"],
    "Erer": ["Fiq", "Lagahida", "Mayaa-muluqo", "Qubi", "Salahad", "Waangaay", "Xamaro", "Yaxoob"],
    "Fafan": ["Awbare", "Babille", "Goljano", "Gursum", "Harawo", "Haroorays", "Harshin", "Jijiga", "Kebri Beyah", "Qooraan", "Shabeeley", "Wajale", "Tuli Guled"],
    "Jarar": ["Araarso", "Awaare", "Bilcil Buur", "Birqod", "Daroor", "Degehabur", "Dhagaxmadow", "Dig", "Gunagado", "Misraq Gashamo", "Yoocaale"],
    "Korahe": ["Boodaley", "Ceel-Ogadeen", "Dobawein", "Higloley", "Kebri Dahar", "Kudunbuur", "Laas-dhankayre", "Marsin", "Shekosh", "Shilavo"],
    "Liben": ["Bokolmayo", "Deka Softi", "Dollo Ado", "Filtu", "Kersa Dula", "Gooro Bakaksa", "Gurra Damole"],
    "Nogob": ["Ayun", "Duhun", "Elweyne", "Gerbo", "Hararey", "Hora-shagax", "Segeg"],
    "Shabelle": ["Abaaqoorow", "Adadle", "Beercaano", "Danan", "Elele", "Ferfer", "Gode", "Imiberi", "Kelafo", "Mustahil"],
    "Sitti": ["Adigala", "Afdem", "Ayesha", "Bike", "Dambal", "Erer", "Gablalu", "Mieso", "Shinile", "Dhunyar", "Daymeed"]
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
    tin = st.text_input("TIN No")
    district = st.selectbox("Degmada (District)", zones[zone])
    kable = st.selectbox("Kable", kable_list)
with col3:
    tax_type = st.selectbox("Nooca Canshuurta", tax_types)
    tax_year = st.selectbox("Sanadka Canshuurta", years)
    date = st.date_input("Taariikhda", datetime.today())

income = st.number_input("Dakhliga Maanta", min_value=0.0, step=0.1)
payment = st.number_input("Lacagta la Bixiyay", min_value=0.0, step=0.1)

if st.button("Kaydi Xogta"):
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
        "Income": income,
        "Payment": payment,
        "Outstanding": income - payment
    }
    df_new = pd.DataFrame([data])

    try:
        df_old = pd.read_csv("dakhli_data.csv")
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    except FileNotFoundError:
        df_all = df_new

    df_all.to_csv("dakhli_data.csv", index=False)
    st.success("Xogta waa la keydiyay ✅")

st.header("Falanqaynta Dakhliga")
try:
    df = pd.read_csv("dakhli_data.csv")
    st.dataframe(df)

    total_clients = df[df['Date'] == str(datetime.today().date())].shape[0]
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

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Xogta Dakhliga Canshuur Bixiyayaasha", ln=True, align="C")
    pdf.ln(10)

    col_width = pdf.w / (len(df.columns) + 1)
    for col_name in df.columns:
        pdf.cell(col_width, 10, txt=col_name, border=1)
    pdf.ln()

    for _, row in df.iterrows():
        for value in row:
            text = str(value)
            if len(text) > 15:
                text = text[:15] + "..."
            pdf.cell(col_width, 10, txt=text, border=1)
        pdf.ln()

    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.download_button(
        label="📥 Soo Degso PDF",
        data=pdf_buffer,
        file_name="dakhli_data.pdf",
        mime="application/pdf"
    )

except FileNotFoundError:
    st.info("Xog lama helin. Fadlan geli xog si aad u aragto falanqayn.")
