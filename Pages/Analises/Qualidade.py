# import streamlit as st
# import pandas as pd
#
#
# def load_data():
#     data = pd.read_csv('IQA2017.csv')
#
#     columns = {'X': 'latitude',
#                'Y': 'longitude',
#                'OBJECTID': 'ID',
#                'codigo': 'codigo',
#                'uf': 'uf',
#                'codigo_anterior': 'versao anterior',
#                'regime': 'regime',
#                'enquadramento': 'enquadramento',
#                'responsavel': 'orgao_responsavel',
#                'latitude': 'latitude',
#                'longitude': 'longitude',
#                'corpo_hidrico': 'nome do rio',
#                'Ano_1': 'ano',
#                'Cont_1': 'contagem',
#                'Media_1': 'media',
#                'Min_1': 'minimo',
#                'Max_1': 'maximo',
#                'Stddev_1': 'stddev',
#                'Variance_1': 'variancia'}
#     data = data.rename(columns=columns)
#
#     data = data[list(columns.values())]
#     #st.write(data)
#
#     return data
#
#
# @st.cache
# def ler_dados():
#     dados = pd.read_csv('tabelaPontosDeColeta.csv')
#     dados = dados.dropna()
#     return dados
#
#
# dados = ler_dados()