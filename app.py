import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

st.set_page_config(page_title="Qalabka Falanqaynta Dakhliga", layout="centered")
st.title("📊 AI Web App – Falanqaynta Dakhliga Maanta")

st.markdown("**Waxaa lagu sameeyay si aad u falanqeyso xogta dakhliga ee Itoobiya – ku saleysan maanta.**")

# Taariikhda maanta
maanta = datetime.date.today()

# Upload CSV ama Geli Xog Toos ah
choice = st.radio("Dooro habka aad xogta gelinayso:", ["📁 Ku shub CSV", "📝 Geli Xog Toos ah"])

if choice == "📁 Ku shub CSV":
    file = st.file_uploader("Fadlan ku shub faylka CSV (magac, taariikh, dakhli, lacag_bixisay):", type="csv")
    if file:
        df = pd.read_csv(file)
        df['taariikh'] = pd.to_datetime(df['taariikh']).dt.date
        df_maanta = df[df['taariikh'] == maanta]
elif choice == "📝 Geli Xog Toos ah":
    st.subheader("Geli xog cusub")
    with st.form("f"):
        magac = st.text_input("Magaca macaamiisha")
        dakhli = st.number_input("Dakhli la helay (Birr)", min_value=0)
        bixisay = st.number_input("Lacag uu bixiyay (Birr)", min_value=0)
        submit = st.form_submit_button("Ku dar xogta")

    if submit:
        df = pd.DataFrame([{
            'magac': magac,
            'taariikh': maanta,
            'dakhli': dakhli,
            'lacag_bixisay': bixisay
        }])
        df_maanta = df

# Haddii xogta maanta jirto
if 'df_maanta' in locals() and not df_maanta.empty:
    st.success(f"Xogta {len(df_maanta)} qof oo maanta yimid ayaa la helay.")

    # Falanqeyn
    total_income = df_maanta['dakhli'].sum()
    df_maanta['lacag_haray'] = df_maanta['dakhli'] - df_maanta['lacag_bixisay']
    lagu_leeyahay = df_maanta[df_maanta['lacag_haray'] > 0]

    st.subheader("📈 Natiijooyinka Maanta")
    st.write(f"**💰 Wadarta dakhliga maanta:** {total_income} Birr")
    st.write(f"**👥 Tirada macaamiisha maanta:** {len(df_maanta)} qof")

    st.subheader("❗ Dadka lacag lagu leeyahay:")
    if lagu_leeyahay.empty:
        st.success("Ma jiro qof lacag lagu leeyahay maanta.")
    else:
        st.write(lagu_leeyahay[['magac', 'lacag_haray']])

    st.subheader("📊 Jaantuska Dakhliga Maanta")
    chart = px.bar(df_maanta, x='magac', y='dakhli', title="Dakhli Qof walba")
    st.plotly_chart(chart)
else:
    st.warning("Fadlan geli xog ama ku shub fayl CSV si aad u aragto natiijooyinka.")
