import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Pages.Analises.TabelaDados as Graficos
import Pages.Analises.DadosFiltrados as Dados


def load_data():
    """
    Carrega os dados de ocorrências aeronáuticas do CENIPA.

    :return: DataFrame com colunas selecionadas.
    """
    columns = {'X': 'latitude',
               'Y': 'longitude',
               'OBJECTID': 'ID',
               'codigo': 'codigo',
               'uf': 'uf',
               'codigo_anterior': 'versao anterior',
               'regime': 'regime',
               'enquadramento': 'enquadramento',
               'responsavel': 'orgao_responsavel',
               'latitude': 'latitude',
               'longitude': 'longitude',
               'corpo_hidrico': 'nome do rio',
               'Ano_1': 'ano',
               'Cont_1': 'contagem',
               'Media_1': 'media',
               'Min_1': 'minimo',
               'Max_1': 'maximo',
               'Stddev_1': 'stddev',
               'Variance_1': 'variancia'}

    data = pd.read_csv('IQA2017.csv')
    data = data.rename(columns=columns)

    data = data[list(columns.values())]

    return data
    st.write(data)


# carregar os dados
df = load_data()
labels = df.uf.unique().tolist()

# SIDEBAR



st.sidebar.title('Menu')
values = ['Graficos','Dados']
Page_Dados = st.sidebar.selectbox('Tratamento de dados', values)


# Parâmetros e número de ocorrências
st.sidebar.header("Parâmetros")
info_sidebar = st.sidebar.empty()  # placeholder, para informações filtradas que só serão carregadas depois

# Slider de seleção do ano
st.sidebar.subheader("Ano")
year_to_filter = st.sidebar.slider('Escolha o ano desejado', 2017)

# Checkbox da Tabela
st.sidebar.subheader("Tabela")
tabela = st.sidebar.empty()  # placeholder que só vai ser carregado com o df_filtered



# Informação no rodapé da Sidebar
st.sidebar.markdown("""
A base de dados de ocorrências aeronáuticas é gerenciada pelo ***Centro de Investigação e Prevenção de Acidentes 
Aeronáuticos (CENIPA)***.
""")


if Page_Dados == 'Graficos':
    Graficos.GraficoEstados()
    st.pyplot()

if Page_Dados == 'Dados':
    Dados.ContagemEnquadramento()
    Dados.ContagemPorEstado()
