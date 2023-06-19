import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Pages import ecologica, integrado, previsaoIqa

st.title("MODV AMBIENTAL - MODELAGEM E ANÁLISE DE RISCO AMBIENTAL")
st.write("**Desenvolvido por Karin de Oliveira**")
st.header("Análise do índice de Qualidade de Água")
st.write("Neste app, são feitas análises dos dados de uma base de dados provenientes do site dados abertos, "
         "onde são armazenados grandes bancos de dados brasileiros e"
         "que ficam liberados para todos.")

st.write("O Índice de Qualidade de Água (IQA) médio anual de um ponto de monitoramento é calculado a partir da média "
         "dos valores"
         "do índice obtidos nas medições realizadas naquele ponto durante o ano. Os valores de IQA calculados "
         "correspondem "
         "aos dados"
         "das próprias entidades responsáveis pelo monitoramento nas Unidades da Federação,"
         "em virtude das variações entre as fórmulas utilizadas para o cálculo,"
         "com o intuito de uniformizar a forma de cálculo do IQA e tornar os valores comparáveis para todo o "
         "território "
         "nacional")

# Create a sidebar section to upload an Excel file
st.sidebar.title("Menu")
uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type="csv")

# Check if a file is uploaded and show the table on the home page
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)

# def load_data():
#     data = pd.read_csv('IQA2017.csv')
#
#     data = data[list(columns.values())]
#     #st.write(data)
#
#     return data
#
#
# @st.cache
# def ler_dados():
#     dados = pd.read_csv('IQA2017.csv')
#     dados = dados.dropna()
#     return dados
#
#
# dados = ler_dados()
#
# # carregar os dados
# df = load_data()
# labels = df.uf.unique().tolist()

# SIDEBAR

st.sidebar.title('Menu')
values = ['Evidência Ecológica', 'Evidência Ecotoxicológica', 'Análise integrada', 'Mapa', 'Previsão IQA']
Page_Dados = st.sidebar.selectbox('Tratamento de dados', values)

# Parâmetros e número de dados
st.sidebar.header("Parâmetros")
info_sidebar = st.sidebar.empty()  # placeholder, para informações filtradas que só serão carregadas depois

# Informação no rodapé da Sidebar
st.sidebar.markdown("""
A base de dados de utilizada se encontra no site ***Dados abertos - Índice de Qualidade de Água***.
""")

if Page_Dados == 'Evidência Ecológica':
    st.title("Evidência Ecológica")
    # ecologica.AnaliseEcologica()

if Page_Dados == 'Evidência Ecotoxicológica':
    st.title("Evidência Ecotoxicológica")

if Page_Dados == 'Risco Integrado':
    st.title("Risco Integrado")
    # integrado.AnaliseIntegrada()

if Page_Dados == 'Previsao':
    st.title('Modelo de previsão do IQA')
    # RegressionModel("MS", "lotico", 2, "Rio Cachoeirão", 2017, 6, 70.6, 75.3, 2.38, 5.65)

if Page_Dados == 'Mapa':
    st.title('Mapa de pontos de coleta')
