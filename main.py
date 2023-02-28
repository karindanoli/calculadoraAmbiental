import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Pages.Analises.TabelaDados as Graficos
import Pages.Analises.DadosFiltrados as Dados
import Pages.Analises.TabelaUnica as Tabela
from Pages.Analises import Cadastro

# from Pages.Analises.Regression import RegressionModel
# from pycaret import load_model, predict_model

st.title("MODV AMBIENTAL - MODELAGEM E ANÁLISE DE RISCO AMBIENTAL")
st.write("**Desenvolvido por Karin de Oliveira**")
st.header("Análise do índice de Qualidade de Água")
st.write("Neste app, são feitas análises dos dados de uma base de dados provenientes do site dados abertos, "
         "onde são armazenados grandes bancos de dados brasileiros e"
         "que ficam liberados para todos.")

st.write("O Índice de Qualidade de Água (IQA) médio anual de um ponto de monitoramento é calculado a partir da média "
         "dos valores"
         "do índice obtidos nas medições realizadas naquele ponto durante o ano. Os valores de IQA calculados correspondem "
         "aos dados"
         "das próprias entidades responsáveis pelo monitoramento nas Unidades da Federação,"
         "em virtude das variações entre as fórmulas utilizadas para o cálculo,"
         "com o intuito de uniformizar a forma de cálculo do IQA e tornar os valores comparáveis para todo o território "
         "nacional")


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
    st.write(data)

    return data


# modelo = load_model('modeloCombinadoDoutorado')

@st.cache
def ler_dados():
    dados = pd.read_csv('IQA2017.csv')
    dados = dados.dropna()
    return dados


dados = ler_dados()

# carregar os dados
df = load_data()
labels = df.uf.unique().tolist()

# SIDEBAR

st.sidebar.title('Menu')
values = ['Tabela', 'Graficos', 'Dados', 'Cadastro']
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

if Page_Dados == 'Cadastro':
    st.title('Cadastro')
    Cadastro.Cadastro()

# if Page_Dados == 'Previsao':
#     st.title('Modelo de previsão do IQA')
#     RegressionModel("MS","lotico",2,"Rio Cachoeirão", 2017, 6,70.6,	75.3,	2.38,	5.65)
#
# if Page_Dados == 'Modelo':
#     st.markdown('---')
#     st.markdown('## **Modelo para Estimar o IQA médio de rios brasileiros**')
#     st.markdown('Utilize as variáveis abaixo para utilizar o modelo de previsão [aqui]().')
#     st.markdown('---')
#
#     col1, col2, col3 = st.beta_columns(3)
#
#     x1 = col1.radio('Estado', dados['Idade'].unique().tolist())
#     x2 = col1.radio('Profissão', dados['Profissão'].unique().tolist())
#     x3 = col1.radio('Tamanho da Empresa', dados['Tamanho da Empresa'].unique().tolist())
#     x4 = col1.radio('Cargo de Gestão', dados['Cargo de Gestão'].unique().tolist())
#     x5 = col3.selectbox('Experiência em DS', dados['Experiência em DS'].unique().tolist())
#     x6 = col2.radio('Tipo de Trabalho', dados['Tipo de Trabalho'].unique().tolist())
#     x7 = col2.radio('Escolaridade', dados['Escolaridade'].unique().tolist())
#     x8 = col3.selectbox('Área de Formação', dados['Área de Formação'].unique().tolist())
#     x9 = col3.selectbox('Setor de Mercado', dados['Setor de Mercado'].unique().tolist())
#     x10 = 1
#     x11 = col2.radio('Estado', dados['Estado'].unique().tolist())
#     x12 = col3.radio('Linguagem Python', dados['Linguagem Python'].unique().tolist())
#     x13 = col3.radio('Linguagem R', dados['Linguagem R'].unique().tolist())
#     x14 = col3.radio('Linguagem SQL', dados['Linguagem SQL'].unique().tolist())
#
#     dicionario = {'Idade': [x1],
#                   'Profissão': [x2],
#                   'Tamanho da Empresa': [x3],
#                   'Cargo de Gestão': [x4],
#                   'Experiência em DS': [x5],
#                   'Tipo de Trabalho': [x6],
#                   'Escolaridade': [x7],
#                   'Área de Formação': [x8],
#                   'Setor de Mercado': [x9],
#                   'Brasil': [x10],
#                   'Estado': [x11],
#                   'Linguagem Python': [x12],
#                   'Linguagem R': [x13],
#                   'Linguagem SQL': [x14]}
#
#     dados = pd.DataFrame(dicionario)
#
#     st.markdown('---')
#     st.markdown(
#         '## **Quando terminar de preencher as informações, clique no botão abaixo para estimar o IQA**')

# if st.button('EXECUTAR O MODELO'):
#     saida = float(predict_model(modelo, dados)['Label'])
#     st.markdown('## IQA **R$ {:.2f}**'.format(saida))
