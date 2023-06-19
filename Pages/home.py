import pandas as pd
import streamlit as st
import iqa.color_classificacao


def app():
    st.title("Home")
    st.markdown(
        """
         Neste app, são feitas análises dos dados de uma base de dados provenientes do site dados abertos,
         onde são armazenados grandes bancos de dados brasileiros e que ficam liberados para todos
 
         Um exemplo de um banco de dados processado abaixo:
    """
    )

    data = {'ID': [1, 2, 3, 4, 5, 6],
            'Pontos de Coleta': ['P0', 'P1', 'P2', 'P3', 'P4', 'P5'],
            'pH': [8.37, 5.47, 8.13, 7.72, 9, 8.73],
            'OD(mg/L)': [10, 12.3, 12, 17.5, 22.5, 13.8],
            'CE(uS/cm2)': [3.6, 394, 1.33, 856, 1.04, 1.12],
            'Turbidez(NTU)': [3.6, 40.8, 21.5, 37.7, 16, 29.7],
            'Temp. liq(Celsius)': [26.5, 28.61, 29.44, 30.21, 31.43, 31.36],
            'ORP(mV)': [144, 287, 79, 91, 79, 69],
            'STD(g/L)': [33, 0.24, 0.85, 0.5, 0.66, 0.71],
            'Salinidade': [0, 2, 2, 2, 1, 1],
            'DQO(mg/L)': [121.3, 454.7, 564.7, 474.7, 324.7, 291.3],
            'DBO(mg/L)': [6.1, 90.9, 112.9, 94.9, 64.9, 58.3],
            'Fosforo(mg/L)': [0.02, 134, 146, 131, 121, 47],
            'Amonia(mg/L)': [0.45, 2.19, 3.21, 1.86, 2.11, 3.27],
            'Nitrato(mg/L)': [0.95, 1.59, 1.89, 1.94, 1.72, 1.47],
            'CT(NMP/100mL)': [7.8, 400, 17000, 2300, 0, 3300],
            'CTE(NMP/100mL)': [7.8, 1100, 54000, 4900, 200, 22000],
            'IQA': [78.8, 34, 27, 32.3, 37.2, 26.7],
            'Classificacao': ['Boa', 'Ruim', 'Ruim', 'Ruim', 'Ruim', 'Ruim']
            }

    df = pd.DataFrame(data)

    styled_table = df.style.applymap(color_classificacao, subset=['Classificacao'])
    st.write(styled_table)

