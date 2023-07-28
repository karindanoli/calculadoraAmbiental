import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

#
# st.title('Mapa de pontos de coleta em GeoJson')
# # Upload
# uploaded_file = st.file_uploader("Upload CSV file", type="xlsx")
# if uploaded_file is not None:
#
#     df = pd.read_excel(uploaded_file)
#
#     # Criando o map em geojson
#     map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
#     my_map = folium.Map(location=map_center, zoom_start=10)
#
#     # Adicionando os pontos
#     for _, row in df.iterrows():
#         folium.Marker(
#             location=[row['Latitude'], row['Longitude']],
#             popup=row['Ponto']
#         ).add_to(my_map)
#
#     folium_static(my_map)
# else:
#     st.info("Please upload a CSV file.")