import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import main as main


def GraficoEstados():
    st.title('Grafico Contagem por Estados')
    plt.figure(figsize=(15, 5))
    plt.hist(main.df.uf, bins=30, rwidth=.8)
    plt.grid()
    st.pyplot(plt)


