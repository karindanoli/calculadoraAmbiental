import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Pages.Analises.TabelaDados as Graficos
import Pages.Analises.DadosFiltrados as Dados
import Pages.Analises.TabelaUnica as Tabela



st.title("MODV AMBIENTAL - MODELAGEM E ANÁLISE DE RISCO AMBIENTAL")
st.write("**Desenvolvido por Karin de Oliveira**")
st.header("Análise do índice de Qualidade de Água")
st.write("Neste app, são feitas análises dos dados de uma base de dados provenientes do site dados abertos, "
         "onde são armazenados grandes bancos de dados brasileiros e"
         "que ficam liberados para todos.")

st.write("O Índice de Qualidade de Água (IQA) médio anual de um ponto de monitoramento é calculado a partir da média dos valores" 
"do índice obtidos nas medições realizadas naquele ponto durante o ano. Os valores de IQA calculados correspondem aos dados" 
"das próprias entidades responsáveis pelo monitoramento nas Unidades da Federação," 
"em virtude das variações entre as fórmulas utilizadas para o cálculo,"
"com o intuito de uniformizar a forma de cálculo do IQA e tornar os valores comparáveis para todo o território nacional")


def load_data():



    data = pd.read_csv('IQA2017.csv')

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
    data = data.rename(columns=columns)

    data = data[list(columns.values())]

    return data
    st.write(data)


# carregar os dados
df = load_data()
labels = df.uf.unique().tolist()

# SIDEBAR

st.sidebar.title('Menu')
values = ['Tabela','Graficos','Dados']
Page_Dados = st.sidebar.selectbox('Tratamento de dados', values)

# Parâmetros e número de dados
st.sidebar.header("Parâmetros")
info_sidebar = st.sidebar.empty()  # placeholder, para informações filtradas que só serão carregadas depois

# Informação no rodapé da Sidebar
st.sidebar.markdown("""
A base de dados de utilizada se encontra no site ***Dados abertos - Índice de Qualidade de Água***.
""")

if Page_Dados == 'Tabela':
    Tabela.TabelaIqa()

if Page_Dados == 'Graficos':
    Graficos.GraficoEstados()
    Graficos.GraficoIQA()

if Page_Dados == 'Dados':
    st.title('Contagem por enquadramento')
    Dados.ContagemEnquadramento()
    st.title('Contagem por Estado')
    Dados.ContagemPorEstado()
    st.title('Contagem Rios por Estado')
    Dados.ContagemRiosEstados()

