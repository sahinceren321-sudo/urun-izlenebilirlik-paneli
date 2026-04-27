import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Ürün Takip", layout="wide")

st.title("Ürün İzlenebilirlik Paneli")

def bekleme_suresi(kayit_saati):
    try:
        baslangic = datetime.strptime(kayit_saati, "%d.%m.%Y %H:%M")
        fark = datetime.now() - baslangic
        gun = fark.days
        saat = fark.seconds // 3600
        dakika = (fark.seconds % 3600) // 60
        return f"{gun} gün {saat} saat {dakika} dk"
    except:
        return "-"

if "veri" not in st.session_state:
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
    st.session_state.veri = pd.DataFrame([
        ["4.9046_51", "Slab", "İç Sahada", "Direkt Slab Satış", "Sevkiyat Bekliyor", simdi],
        ["4.4244_52", "Kütük", "Kütük Sahada", "Kangal Oldu", "Kangal Haddehanesine Gidecek", simdi],
    ], columns=["Ürün ID", "Tip", "Konum", "Durum", "Sonraki Adım", "Kayıt Saati"])

df = st.session_state.veri.copy()
df["Bekleme Süresi"] = df["Kayıt Saati"].apply(bekleme_suresi)

st.subheader("Genel Tablo")

# Başlıklar
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([2,2,2,2,2,2,2,1])
col1.write("Ürün ID")
col2.write("Tip")
col3.write("Konum")
col4.write("Durum")
col5.write("Sonraki Adım")
col6.write("Kayıt Saati")
col7.write("Bekleme Süresi")
col8.write("Sil")

st.markdown("---")

# Satırlar
for i, row in st.session_state.veri.iterrows():
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([2,2,2,2,2,2,2,1])

    col1.write(row["Ürün ID"])
    col2.write(row["Tip"])
    col3.write(row["Konum"])
    col4.write(row["Durum"])
    col5.write(row["Sonraki Adım"])
    col6.write(row["Kayıt Saati"])
    col7.write(bekleme_suresi(row["Kayıt Saati"]))

    if col8.button("🗑️", key=f"sil_{i}"):
        st.session_state.veri = st.session_state.veri.drop(i).reset_index(drop=True)
        st.rerun()
st.subheader("Yeni Veri Girişi")

with st.form("form"):
    urun = st.text_input("Ürün ID")

    tip = st.selectbox("Tip", ["Slab", "Kütük", "Kangal", "Levha"])

    konum = st.selectbox("Konum", [
        "İç Sahada",
        "Dış Sahada",
        "Liman Sahada",
        "Uzak Sahada",
        "Dış Sahada (BC)",
        "Kütük Depoda"
    ])

    durum = st.selectbox("Durum", [
        "Levha Oldu",
        "Kangal Oldu",
        "Direkt Slab Satış"
    ])

    adim = st.selectbox("Sonraki Adım", [
        "Sevkiyat Bekliyor",
        "Sıcak Haddehaneye Gidecek",
        "Kangal Haddehanesine Gidecek"
    ])

    kaydet = st.form_submit_button("Kaydet")

if kaydet:
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M")

    yeni = pd.DataFrame([
        [urun, tip, konum, durum, adim, simdi]
    ], columns=["Ürün ID", "Tip", "Konum", "Durum", "Sonraki Adım", "Kayıt Saati"])

    st.session_state.veri = pd.concat(
        [st.session_state.veri, yeni],
        ignore_index=True
    )

    st.success("Kayıt eklendi")
    st.rerun()
