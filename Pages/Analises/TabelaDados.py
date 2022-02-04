import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import main as main


def GraficoEstados():
    st.title('Grafico Contagem por Estados')
    plt.figure(figsize=(15, 5))
    plt.hist(main.df.uf, bins=30, rwidth=.8, color='g')
    plt.grid()
    st.pyplot(plt)

def GraficoIQA():
    st.title('Grafico Correlação IQA ')
    plt.figure(figsize=(15, 5))
    estado = main.df.loc[main.df['uf'] == 'PE']
    a = estado['media']
    b = estado['maximo']
    plt.scatter(a, b)
    plt.grid()
    st.pyplot(plt)



