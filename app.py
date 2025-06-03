import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import io
from docx import Document

# Connect to SQLite DB (file will be created if doesn't exist)
conn = sqlite3.connect('dakhli_data.db', check_same_thread=False)
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS dakhli (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Magaca TEXT,
    TIN TEXT,
    Mobile TEXT,
    Zone TEXT,
    District TEXT,
    Kable TEXT,
    Tax_Type TEXT,
    Tax_Year TEXT,
    Date TEXT,
    Income REAL,
    Payment REAL,
    Outstanding REAL
)
''')
conn.commit()

# Your current UI code remains the same, then when saving data:

if st.button("Kaydi Xogta"):
    if not tin.isdigit() or len(tin) != 10:
        st.error("Fadlan geli TIN sax ah (10 lambar)")
    else:
        outstanding = income - payment
        c.execute('''
            INSERT INTO dakhli (Magaca, TIN, Mobile, Zone, District, Kable, Tax_Type, Tax_Year, Date, Income, Payment, Outstanding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, tin, mobile, zone, district, kable, tax_type, tax_year, date.strftime('%Y-%m-%d'), income, payment, outstanding))
        conn.commit()
        st.success("Xogta waa la keydiyay ✅")

st.header("Falanqaynta Dakhliga")

# Fetch all data from DB
df = pd.read_sql_query("SELECT * FROM dakhli", conn)

if df.empty:
    st.info("Xog lama helin. Fadlan geli xog si aad u aragto falanqayn.")
else:
    st.dataframe(df)

    today = datetime.today().strftime('%Y-%m-%d')
    total_clients = df[df['Date'] == today].shape[0]
    total_income = df['Income'].sum()
    total_outstanding = df['Outstanding'].sum()

    st.metric("Tirada Canshuur Bixiyayaasha Maanta", total_clients)
    st.metric("Dakhliga Guud", f"{total_income:,.2f}")
    st.metric("Lacagta aan wali la Bixin", f"{total_outstanding:,.2f}")

    import plotly.express as px
    fig = px.bar(df, x='Date', y='Income', color='Tax_Type', title='Dakhliga Maalinlaha ah')
    st.plotly_chart(fig, use_container_width=True)

    # Excel download
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine='xlsxwriter')
    st.download_button(
        label="📥 Soo Degso Excel",
        data=excel_buffer.getvalue(),
        file_name="dakhli_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Word download
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
