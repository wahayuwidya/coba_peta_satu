import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import random

# Fungsi untuk membaca file excel dan mengubahnya menjadi DataFrame
def load_data(uploaded_file):
    data = pd.read_excel(uploaded_file)
    return data

# Fungsi untuk menyesuaikan koordinat yang sama
def adjust_coordinates(lat, lon, offset=0.00001):  # Meningkatkan offset
    return lat + random.uniform(-offset, offset), lon + random.uniform(-offset, offset)

# Fungsi untuk membuat peta folium
def create_map(data, selected_pelatihan):
    m = folium.Map(location=[-2.5489, 118.0149], zoom_start=5)  # Lokasi pusat Indonesia

    # Marker Cluster untuk mengelompokkan marker
    marker_cluster = MarkerCluster().add_to(m)

    # Menambahkan marker ke peta
    for _, row in data.iterrows():
        if selected_pelatihan == 'Semua' or row['Nama Pelatihan'] == selected_pelatihan:
            # Menggeser koordinat jika ada yang sama
            lat, lon = adjust_coordinates(row['Latitude'], row['Longitude'])

            # Isi NIP dengan "-" jika kosong
            nip = row['NIP'] if pd.notna(row['NIP']) and row['NIP'] != '' else '-'

            popup_text = (f"<div style='width: 250px;'>"
                          f"<b>Nama:</b> {row['Nama']}<br>"
                          f"<b>NIP:</b> {nip}<br>"
                          f"<b>NIK:</b> {row['NIK']}<br>"
                          f"<b>Usia:</b> {row['Usia']}<br>"
                          f"<b>Jenis Kelamin:</b> {row['Jenis Kelamin']}<br>"
                          f"<b>Pendidikan Terakhir:</b> {row['Pendidikan Terakhir']}<br>"
                          f"<b>Nama Pelatihan:</b> {row['Nama Pelatihan']}<br>"
                          f"<b>Jenis Pelatihan:</b> {row['Jenis Pelatihan']}<br>"
                          f"<b>Tahun:</b> {row['Tahun']}<br>"
                          f"<b>Alamat:</b> {row['Alamat']}<br>"
                          f"<b>Provinsi Asal:</b> {row['Provinsi Asal']}</div>")

            folium.Marker(
                location=[lat, lon],
                icon=folium.Icon(icon='info-sign'),  # Hapus penetapan warna
                popup=folium.Popup(popup_text, max_width=300)  # Pop-up lebih lebar
            ).add_to(marker_cluster)
    
    return m

st.title("Peta Persebaran Domisili Purnawidya")

# Upload file excel
uploaded_file = st.file_uploader("Upload file Excel", type=["xlsx"])

if uploaded_file is not None:
    data = load_data(uploaded_file)
    st.dataframe(data)

    # Menampilkan pilihan nama pelatihan
    pelatihan_options = ['Semua'] + list(data['Nama Pelatihan'].unique())
    selected_pelatihan = st.selectbox("Pilih Nama Pelatihan", pelatihan_options)

    # Buat peta dengan data yang dipilih
    map_data = data if selected_pelatihan == 'Semua' else data[data['Nama Pelatihan'] == selected_pelatihan]
    map_object = create_map(map_data, selected_pelatihan)
    
    # Tampilkan peta
    folium_static(map_object)
