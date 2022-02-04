import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import main as main


def ContagemEnquadramento():

    st.write(main.df.enquadramento.value_counts())

def ContagemPorEstado():

    st.write(main.df.loc[main.df.uf == 'RJ'].uf.value_counts())

def ContagemRiosEstados():

    st.write(main.df.uf.value_counts())

