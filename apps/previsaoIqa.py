# import streamlit as st
# import pandas as pd
# import joblib
# import pycaret
#
# modelo = joblib.load('modeloCombinadoDoutorado.pkl')
#
# st.title('Previsão IQA')
# # Upload
# uploaded_file = st.file_uploader("Upload XLSX file", type="xlsx")
# if uploaded_file is not None:
#     df = pd.read_excel(uploaded_file)
#
#     uf = df['uf'].values[0]
#     regime = df['regime'].values[0]
#     enquadramento = df['enquadramento'].values[0]
#     corpo_hidrico = df['corpo_hidrico'].values[0]
#     ano = df['ano'].values[0]
#     contagem = df['contagem'].values[0]
#     minimo = df['minimo'].values[0]
#     maximo = df['maximo'].values[0]
#     stddev = df['stddev'].values[0]
#     variancia = df['variancia'].values[0]
#
#     dados0 = {'uf': [uf], 'regime': [regime], 'enquadramento': [enquadramento], 'corpo_hidrico': [corpo_hidrico],
#               'ano': [ano], 'contagem': [contagem], 'minimo': [minimo], 'maximo': [maximo], 'stddev': [stddev],
#               'variancia': [variancia]}
#     dados = pd.DataFrame(dados0)
#
#     pred = float(modelo.predict(dados).round(2))
#
#     st.write(f'O IQA MÉDIO É DE: {pred}')
