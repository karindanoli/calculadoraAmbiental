from typing import Dict, Any
from utils import download
from utils import uploadFiles
import base64

import numpy as np
import pandas as pd
import streamlit as st
from loguru import logger


def create_table():
    st.subheader("Complete a tabela abaixo:")
    st.write("Valores de coluna são separados por vírgula "
             "(E.g: se preencher o ID com os valores 1,2, "
             "a tabela terá o valor 1 na col 1 e 2 na col 2)")
    st.write("ATENÇÃO: Não coloque espaço entre vírgulas(E.g: 1, 2)")
    st.write("Preencha todos os campos, o cálculo só será correto com todos os valores")
    st.write("Use somente valores alfanuméricos (A-Z,0-9)")

    if 'reset_key' not in st.session_state:
        st.session_state.reset_key = 0

    default_values = {
        "ID": "", "Pontos de Coleta": "", "P0_BPS": "", "BPS": "", "P0_BPA": "", "BPA": "", "P0_Dietilftalato": "",
        "Dietilftalato": "", "P0_Benzofenona": "", "Benzofenona": ""}

    with st.form(key="table_form"):
        input_data: Dict[Any, Any] = {}
        input_containers = {}

        for key in default_values.keys():
            input_containers[key] = st.empty()
            input_data[key] = input_containers[key].text_input(key, default_values[key],
                                                               key=f"{key}_input_{st.session_state.reset_key}")

        create_table_button = st.form_submit_button("Criar tabela")
        clear_table_button = st.form_submit_button("Limpar tabela")

    if create_table_button:
        # Split input values by comma and create a list of dictionaries
        input_rows = []
        for i in range(len(input_data["ID"].split(","))):
            row = {}
            for key in default_values.keys():
                values = input_data[key].split(",")
                row[key] = values[i].strip() if i < len(values) else ""
            input_rows.append(row)

        dataframe = pd.DataFrame(input_rows)
        st.session_state.user_created_table = dataframe
        st.write(dataframe)
        return dataframe
    else:
        st.write("Preencha a tabela e clique em 'Criar tabela' para visualizar os dados. ")

    if clear_table_button:
        st.session_state.reset_key += 1
        st.experimental_rerun()


def download_template():
    example = pd.DataFrame(columns=["ID", "Pontos de Coleta", "BPS", "BPA", "Dietilftalato", "Benzofenona"])
    csv = example.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="tabelaTemplate.csv">Download tabelaTemplate.csv</a>'


def leng_data(dataframe):
    length = len(dataframe)
    return length


def BPS(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):
        if column == 'BPS':
            result_BPS = 1 / (1 + np.exp((np.log(0.1) - np.log(pd.to_numeric(value_df))) / 0.4))
            result_BPS_final = (result_BPS - 0.1) / (1 - 0.1)
            print(result_BPS, "BPS", result_BPS_final, value_df)
            return result_BPS_final


def BPA(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):
        if column == 'BPA':
            result_BPA = 1 / (1 + np.exp((np.log(0.175) - np.log(pd.to_numeric(value_df))) / 0.4))
            result_BPA_final = (result_BPA - 0.45) / (1 - 0.45)
            print(result_BPA, "BPA", result_BPA_final, value_df)
            return result_BPA_final


def Dietilftalato(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):
        if column == 'Dietilftalato':
            result_Dietilftalato = 1 / (1 + np.exp((np.log(5) - np.log(pd.to_numeric(value_df))) / 0.4))
            result_Dietilftalato_final = (result_Dietilftalato - 0.29) / (1 - 0.29)
            print(result_Dietilftalato, "Dietilftalato", result_Dietilftalato_final, value_df)
            return result_Dietilftalato_final


def Benzofenona(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):
        if column == 'Benzofenona':
            result_Benzofenona = 1 / (1 + np.exp((np.log(3) - np.log(pd.to_numeric(value_df))) / 0.4))
            result_Benzofenona_final = (result_Benzofenona - 0.02) / (1 - 0.02)
            print(result_Benzofenona, "Benzofenona", result_Benzofenona_final, value_df)
            return result_Benzofenona_final


def risco_quimico(dataframe):
    for i in range(len(dataframe)):
        print(i)
        print(len(dataframe))

        dataframe["RISCO"] = 1 - ((1 - BPS(dataframe)) * (1 - BPA(dataframe)) * (1 - Dietilftalato(dataframe)) * (
                1 - Benzofenona(dataframe)))
        return dataframe["RISCO"]


def calculate_eco(dataframe):
    for i in range(len(dataframe)):
        print(i)
        print(len(dataframe))

        dataframe["RISCO"] = 1 - ((1 - BPS(dataframe)) * (1 - BPA(dataframe)) * (1 - Dietilftalato(dataframe)) * (
                    1 - Benzofenona(dataframe)))
        print(dataframe["RISCO"][0])
        print(BPA(dataframe))

        conditions = [
            (dataframe["RISCO"] >= 0.76),
            (dataframe["RISCO"] >= 0.51) & (dataframe["RISCO"] <= 0.75),
            (dataframe["RISCO"] >= 0.26) & (dataframe["RISCO"] <= 0.50),
            (dataframe["RISCO"] >= 0) & (dataframe["RISCO"] <= 0.25)
        ]

        classifications = ["inexistente", "moderado", "moderado", "extremo"]

        dataframe["Classificacao"] = np.select(conditions, classifications, default=0)

        final_result_quimica = np.mean(dataframe["RISCO"])
        st.session_state.final_result_quimica = final_result_quimica

        return dataframe


def color_classificacao(val):
    color = ''
    if val == 'inexistente':
        color = 'blue'
    elif val == 'moderado':
        color = 'green'
    elif val == 'moderado':
        color = 'yellow'
    elif val == 'extremo':
        color = 'red'

    return f'background-color: {color}'


def app():
    """
    A página é criada aqui
    """
    st.title("Calcular loe quimica")
    st.header("Use APENAS UMA das opções abaixo:")
    st.write("Use uma opção e então clique no botão 'Processar tabela' no fundo para calcular IQA")

    # URL and file uploader inputs
    url = st.empty()
    url_input = url.text_input("Insira uma URL para uma tabela .csv válida", "")

    data = st.empty()
    file_uploader = data.file_uploader("Faça upload de tabela .csv", type=["csv"])

    # Clear URL and file uploader inputs
    clear_url_button = st.button("Limpar URL")
    clear_file_button = st.button("Limpar arquivo")

    if clear_url_button:
        url_input = url.text_input("Insira uma URL para uma tabela .csv válida", "", key="url_input")

    if clear_file_button:
        file_uploader = data.file_uploader("Faça upload de tabela .csv", type=["csv"], key="file_uploader")

    st.markdown(download_template(), unsafe_allow_html=True)

    create_table()

    process_table_button = st.button("Processar Tabela")

    if process_table_button:
        user_created_table = st.session_state.get('user_created_table', None)
        if file_uploader or url_input or user_created_table is not None:
            try:
                if file_uploader:
                    file_path = uploadFiles.save_uploaded_file(file_uploader, file_uploader.name)
                    dataframe = pd.read_csv(file_path, encoding='utf-8')
                    logger.info("data", dataframe)
                elif url_input:
                    file_path = url_input
                    dataframe = pd.read_csv(file_path, encoding='utf-8')
                    logger.info("url", dataframe)
                elif user_created_table is not None:
                    dataframe = user_created_table
                    logger.info("user created", dataframe)
                else:
                    raise ValueError("Nenhuma tabela foi fornecida.")

                df = calculate_eco(dataframe)
                st.header("Análise IQA pronta - tabela disponível para download")
                styled_table = df.style.applymap(color_classificacao, subset=['Classificacao'])
                st.write(styled_table.to_html(escape=False), unsafe_allow_html=True)
                st.markdown(download.get_table_download_link(df), unsafe_allow_html=True)

            except (UnicodeDecodeError, ValueError) as e:
                st.error(str(e))
                logger.error(str(e))
                return
        else:
            st.error("Nenhuma tabela foi fornecida. Por favor, forneça uma tabela.")

#
#
# st.markdown("Explicação sobre o calculo de evidência ecológica")
#
# # Cria tabela
# data = {
# "Referencia": [10, 957, 50],
# "Ponto 1": [8, 750, 38],
# "Ponto 2": [5, 233, 10]
# }
#
# df = pd.DataFrame(data, index=["Taxa (No.)", "Indivíduos (No.)", "Microalgas (%)"])
#
#
# st.table(df)
#
# # Coleta valores da tabela
# ref_values = df["Referencia"]
# site_a_values = df["Ponto 1"]
# site_b_values = df["Ponto 2"]
#
# # divisão do valor da amostra pelo valor de referência.
# taxa_a = site_a_values / ref_values
# taxa_b = site_b_values / ref_values
#
# # Calcula o log (R1)
# log_a = abs(taxa_a.apply(math.log10))
# log_b = abs(taxa_b.apply(math.log10))
#
# # Calcula a soma dos logs e multiplicca por -1
# result_a = -1 * log_a.sum()
# result_b = -1 * log_b.sum()
#
# # calcula o n para a média
# num_valores = len(df.columns)
#
# # Finaliza a BKX_Triad
# bkx_triad_a = 1 - math.pow(10, (result_a / num_valores))
# bkx_triad_b = 1 - math.pow(10, (result_b / num_valores))
#
# # Display the results
# results_data = {
# "Referencia": [0, 0, 0],
# "Ponto 1": [0, result_a, bkx_triad_a],
# "Ponto 2": [0, result_b, bkx_triad_b]
# }
#
# results_df = pd.DataFrame(results_data, index=["Referencia", "Ponto 1", "Ponto 2"])
# st.table(results_df)
#
# # grafico
# fig = go.Figure()
# for column in results_df.columns:
#     fig.add_trace(go.Bar(x=[column], y=[results_df[column][1]], name=column))
#
# fig.update_layout(
#     title="Results",
#     xaxis_title="Columns",
#     yaxis_title="Result",
#     width=600,
#     height=400
# )
#
# st.plotly_chart(fig)
