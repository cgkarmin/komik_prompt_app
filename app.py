import streamlit as st
from datetime import datetime
import pandas as pd
import os

# Konfigurasi fail & folder
st.set_page_config(page_title="Penjana Panel Komik AI", layout="centered")
csv_path = "data/panel_komik.csv"
os.makedirs("data", exist_ok=True)

st.title("🎨 Penjana Panel Komik AI")
st.caption("Edisi Cikgu Karmin — Fokus pada Watak: Pak Leman & Pak Mail")

# ========== FORM INPUT UNTUK 1 PANEL ========== #

with st.form("panel_form"):
    st.subheader("🖼️ Maklumat Panel Komik")

    watak_panel = st.multiselect(
        "🧍 Watak dalam Panel",
        ["Pak Leman", "Pak Mail"],
        default=["Pak Leman"]
    )

    latar_belakang = st.text_input("🌄 Latar Belakang / Ilustrasi", "Contoh: Masjid lama waktu pagi")

    aksi = st.text_input("🎬 Aksi dalam Panel", "Contoh: Pak Leman sedang memarahi Pak Mail yang lambat")

    dialog_leman = st.text_input("💬 Dialog Pak Leman", "Contoh: 'Mail, kau ingat masjid ni hotel ke?'")
    dialog_mail = st.text_input("💬 Dialog Pak Mail", "Contoh: 'Maaf, Lem... terlewat sikit.'")

    saiz_panel = st.selectbox("📐 Saiz Panel", ["Landskap", "Potret", "Empat Segi"])

    teks_tambahan = st.text_input("📝 Teks Tambahan dalam Panel", "Contoh: 'Pagi Jumaat yang penuh peringatan'")

    gaya_lukisan = st.selectbox("🎨 Gaya Lukisan", [
        "Pop Art Melayu",
        "70% Ghibli Melayu",
        "Hitam Putih Tebal",
        "Pensil Sketsa Kampung",
        "Flat Minimalis",
        "Komik Tradisional Melayu",
        "Watercolor (Cat Air Lembut)",
        "Gaya LAT (Inspired by Lat)"
    ])

    # Kulit Muka (optional untuk panel pertama)
    with st.expander("📕 Penjana Kulit Muka (Opsyenal)", expanded=False):
        judul = st.text_input("📘 Judul", "")
        subjudul = st.text_input("📗 Sub-Judul", "")
        deskripsi = st.text_area("📄 Deskripsi Cerita", "")

    submitted = st.form_submit_button("Jana Prompt Panel Ini")

# ========== OUTPUT ========== #
if submitted:
    tarikh = datetime.now().strftime("%Y-%m-%d")
    waktu = datetime.now().strftime("%H:%M")

    watak_str = ", ".join(watak_panel)
    dialog_full = ""
    if dialog_leman: dialog_full += f"Pak Leman: \"{dialog_leman}\"\n"
    if dialog_mail: dialog_full += f"Pak Mail: \"{dialog_mail}\""

    # Hasilkan prompt teks AI
    prompt = f"""
Panel komik ini menunjukkan {watak_str} di latar: {latar_belakang}.
Aksi yang berlaku: {aksi}.
Saiz panel: {saiz_panel}.
Gaya lukisan: {gaya_lukisan}.
Teks tambahan: {teks_tambahan}.

Dialog:
{dialog_full}
""".strip()

    if judul or subjudul or deskripsi:
        prompt = f"""
== KULIT MUKA ==
Judul: {judul}
Sub-Judul: {subjudul}
Deskripsi: {deskripsi}

== PANEL ==
{prompt}
""".strip()

    st.success("✅ Prompt berjaya dijana!")
    st.code(prompt, language="markdown")

    # Simpan ke CSV
    panel_data = {
        "Tarikh": tarikh,
        "Waktu": waktu,
        "Watak": watak_str,
        "Latar Belakang": latar_belakang,
        "Aksi": aksi,
        "Dialog": dialog_full,
        "Saiz Panel": saiz_panel,
        "Teks Tambahan": teks_tambahan,
        "Gaya Lukisan": gaya_lukisan,
        "Judul": judul,
        "Sub-Judul": subjudul,
        "Deskripsi": deskripsi,
        "Prompt": prompt
    }

    df_new = pd.DataFrame([panel_data])
    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        df_all = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_all = df_new

    df_all.to_csv(csv_path, index=False)

    with st.expander("📜 Lihat Semua Prompt Terdahulu"):
        st.dataframe(df_all)

