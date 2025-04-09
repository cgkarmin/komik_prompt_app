import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

# Konfigurasi laluan fail
st.set_page_config(page_title="Penjana Panel Komik Dwibahasa", layout="centered")
csv_path = "data/panel_komik.csv"
json_folder = "data/prompt_json"
os.makedirs(json_folder, exist_ok=True)

st.title("🧾 Penjana Panel Komik Dwibahasa + JSON")
st.caption("Edisi Cikgu Karmin — Format Siap Guna AI & Manusia")

# Fungsi untuk memaparkan kandungan JSON
def paparkan_panel_json(json_data):
    watak_str = ", ".join(json_data['panel']['characters'])
    st.markdown("### 🇲🇾 Versi Bahasa Melayu")
    blok_bm = (
        f"== KULIT MUKA ==\n"
        f"Judul: {json_data['title']['ms']}\n"
        f"Sub-Judul: {json_data['subtitle']['ms']}\n"
        f"Deskripsi: {json_data['description']['ms']}\n\n"
        f"== PANEL ==\n"
        f"Panel komik ini menunjukkan {watak_str} di latar: {json_data['panel']['background']['ms']}.\n"
        f"Aksi yang berlaku: {json_data['panel']['action']['ms']}.\n"
        f"Saiz panel: {json_data['panel']['panel_size']}.\n"
        f"Gaya lukisan: {json_data['panel']['drawing_style']}.\n"
        f"Teks tambahan: {json_data['panel']['extra_text']['ms']}.\n\n"
        f"Dialog:\n"
        f"Pak Leman: \"{json_data['panel']['dialog']['Pak Leman']['ms']}\"\n"
        f"Pak Mail: \"{json_data['panel']['dialog']['Pak Mail']['ms']}\""
    )
    st.code(blok_bm, language="markdown")

    st.markdown("### 🇬🇧 English Version")
    blok_en = (
        f"== COVER ==\n"
        f"Title: {json_data['title']['en']}\n"
        f"Sub-Title: {json_data['subtitle']['en']}\n"
        f"Description: {json_data['description']['en']}\n\n"
        f"== PANEL ==\n"
        f"This comic panel shows {watak_str} at the background: {json_data['panel']['background']['en']}.\n"
        f"Action: {json_data['panel']['action']['en']}.\n"
        f"Panel size: {json_data['panel']['panel_size']}.\n"
        f"Drawing style: {json_data['panel']['drawing_style']}.\n"
        f"Extra text: {json_data['panel']['extra_text']['en']}.\n\n"
        f"Dialog:\n"
        f"Pak Leman: \"{json_data['panel']['dialog']['Pak Leman']['en']}\"\n"
        f"Pak Mail: \"{json_data['panel']['dialog']['Pak Mail']['en']}\""
    )
    st.code(blok_en, language="markdown")

# Papar pilihan fail JSON tersimpan
st.sidebar.header("📂 Buka Panel Tersimpan")
json_files = [f for f in os.listdir(json_folder) if f.endswith(".json")]
selected_file = st.sidebar.selectbox("Pilih fail JSON", [""] + json_files)

if selected_file:
    with open(os.path.join(json_folder, selected_file), "r", encoding="utf-8") as f:
        data_loaded = json.load(f)
        paparkan_panel_json(data_loaded)
        st.download_button("📦 Muat Turun JSON Ini", json.dumps(data_loaded, ensure_ascii=False, indent=2), file_name=selected_file, mime="application/json")

st.markdown("---")
st.header("🖊️ Jana Panel Baharu")

# Borang input baharu
with st.form("panel_form"):
    watak_panel = st.multiselect("🧍 Watak dalam Panel", ["Pak Leman", "Pak Mail"], default=["Pak Leman"])
    latar_belakang = st.text_input("🌄 Latar Belakang (BM)", "Masjid lama waktu pagi")
    latar_en = st.text_input("🌄 Background (EN)", "Old mosque in the morning")
    aksi = st.text_input("🎬 Aksi (BM)", "Pak Leman sedang memarahi Pak Mail yang lambat")
    aksi_en = st.text_input("🎬 Action (EN)", "Pak Leman scolding Pak Mail for being late")
    dialog_leman_bm = st.text_input("💬 Dialog Pak Leman (BM)", "Mail, kau ingat masjid ni hotel ke?")
    dialog_leman_en = st.text_input("💬 Dialog Pak Leman (EN)", "Mail, you think this mosque is a hotel?")
    dialog_mail_bm = st.text_input("💬 Dialog Pak Mail (BM)", "Maaf, Lem... terlewat sikit.")
    dialog_mail_en = st.text_input("💬 Dialog Pak Mail (EN)", "Sorry, Lem... just a bit late.")
    saiz_panel = st.selectbox("📐 Saiz Panel", ["Landskap", "Potret", "Empat Segi"])
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
    teks_tambahan_bm = st.text_input("📝 Teks Tambahan (BM)", "Pagi Jumaat yang penuh peringatan")
    teks_tambahan_en = st.text_input("📝 Extra Text (EN)", "A Friday morning full of reminders")

    with st.expander("📕 Kulit Muka"):
        judul = st.text_input("📘 Judul", "PAK PAK BIM BING")
        subjudul = st.text_input("📗 Sub-Judul", "Masa Itu Emas")
        deskripsi_bm = st.text_area("📄 Deskripsi (BM)", "Lambat bukan masalah. Lambat tu gejala penyakit. Penyakitnya malas.")
        deskripsi_en = st.text_area("📄 Description (EN)", "Being late is not the problem. It’s a symptom. The disease is laziness.")

    submitted = st.form_submit_button("Jana Prompt & Simpan")

if submitted:
    waktu = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    json_data = {
        "title": {"ms": judul, "en": judul},
        "subtitle": {"ms": subjudul, "en": subjudul},
        "description": {"ms": deskripsi_bm, "en": deskripsi_en},
        "panel": {
            "characters": watak_panel,
            "background": {"ms": latar_belakang, "en": latar_en},
            "action": {"ms": aksi, "en": aksi_en},
            "panel_size": saiz_panel,
            "drawing_style": gaya_lukisan,
            "extra_text": {"ms": teks_tambahan_bm, "en": teks_tambahan_en},
            "dialog": {
                "Pak Leman": {"ms": dialog_leman_bm, "en": dialog_leman_en},
                "Pak Mail": {"ms": dialog_mail_bm, "en": dialog_mail_en}
            }
        }
    }

    json_filename = f"panel_{waktu}.json"
    json_path = os.path.join(json_folder, json_filename)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    st.success(f"✅ Panel berjaya disimpan sebagai {json_filename}")
    paparkan_panel_json(json_data)
    st.download_button("📦 Muat Turun .json", json.dumps(json_data, ensure_ascii=False, indent=2), file_name=json_filename, mime="application/json")
