import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import main as main


def TabelaIqa():
    df = pd.read_csv('IQA2017.csv')
    st.table(df)
