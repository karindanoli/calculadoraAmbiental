import streamlit as st
import pandas as pd
import joblib

modelo = joblib.load('modeloCombinadoDoutorado.pkl')

def RegressionModel(uf, regime, enquadramento, corpo_hidrico, ano, contagem, minimo, maximo, stddev, variancia):
    dados0 = {'uf': [uf], 'regime': [regime], 'enquadramento': [enquadramento], 'corpo_hidrico': [corpo_hidrico],
              'ano': [ano], 'contagem': [contagem], 'minimo': [minimo], 'maximo': [maximo], 'stddev': [stddev],
              'variancia': [variancia]}
    dados = pd.DataFrame(dados0)

    pred = float(modelo.predict(dados).round(2))

    st.write(f'O IQA MÉDIO É DE: {pred}')