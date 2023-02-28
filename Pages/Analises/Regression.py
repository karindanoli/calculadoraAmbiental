import streamlit as st
import pandas as pd
from pycaret.classification import load_model

modelo = load_model('modeloCombinadoDoutorado')


def RegressionModel(uf, regime, enquadramento, corpo_hidrico, ano, contagem, minimo, maximo, stddev, variancia):
    dados0 = {'uf': [uf], 'regime': [regime], 'enquadramento': [enquadramento], 'corpo_hidrico': [corpo_hidrico],
              'ano': [ano], 'contagem': [contagem], 'minimo': [minimo], 'maximo': [maximo], 'stddev': [stddev],
              'variancia': [variancia]}
    dados = pd.DataFrame(dados0)

    pred = float(pd.predict_model(modelo, data=dados)['Label'].round(2))

    print('O IQA MÉDIO É DE: ${}'.format(pred))
