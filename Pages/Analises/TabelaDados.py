import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import main as main


def GraficoEstados():
    plt.figure(figsize=(15, 5))
    main.df.uf.value_counts().iloc[:2].plot()
    plt.grid()

