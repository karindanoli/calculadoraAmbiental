import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import main as main


def Cadastro():
    with st.form(key= "include_data"):
        input_name = st.text_input(label="Insira o nome do corpo hídrico")
        input_ano = st.text_input(label="Insira o ano")
        input_uf = st.text_input(label="Insira UF")
        input_media = st.text_input(label="Insira IQA médio")
        input_minimo = st.text_input(label="Insira IQA minimo")
        input_maximo = st.text_input(label="Insira IQA maximo")
        input_button =st.form_submit_button("Salvar cadastro")

    if input_button:
        st.write('Corpo hidrico: {input_name}')
        st.write('Ano: {input_ano}')
        st.write('UF: {input_uf}')
        st.write('IQA médio: {input_media}')
        st.write('IQA minimo: {input_minimo}')
        st.write('IQA maximo: {input_maximo}')