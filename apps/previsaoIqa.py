import streamlit as st
import pandas as pd
import joblib
import pycaret.regression

def app():
    modelo = joblib.load('modeloCombinadoDoutorado.pkl')

    st.title('Previsão')
    # Upload
    # uploaded_file = st.file_uploader("Upload XLSX file", type="xlsx")
    # if uploaded_file is not None:
    df = pd.read_excel('IQA2017_tratada.xlsx')

    uf = df['uf']
    regime = df['regime']
    enquadramento = df['enquadramento']
    corpo_hidrico = df['corpo_hidrico']
    ano = df['ano']
    contagem = df['contagem']
    media = df['media']
    minimo = df['minimo']
    maximo = df['maximo']
    stddev = df['stddev']
    variancia = df['variancia']

    dados0 = {'uf': [uf], 'regime': [regime], 'enquadramento': [enquadramento], 'corpo_hidrico': [corpo_hidrico],
              'ano': [ano], 'contagem': [contagem], 'media': [media], 'minimo': [minimo], 'maximo': [maximo], 'stddev': [stddev],
              'variancia': [variancia]}
    dados = pd.DataFrame(dados0)

    pred = float(modelo.predict(dados).round(2))

    st.write(f'O IQA MÉDIO É DE: {pred}')
