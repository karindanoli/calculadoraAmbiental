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
        "ID": "", "Pontos de Coleta": "", "Controle_Clorella": "", "Chlorella": "", "Controle_Ceriodaphnia": "",
        "Ceriodaphnia": ""}

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
    example = pd.DataFrame(
        columns=["ID", "Pontos de Coleta", "Controle_Clorella", "Chlorella", "Controle_Ceriodaphnia", "Ceriodaphnia"])
    csv = example.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="tabelaTemplate.csv">Download tabelaTemplate.csv</a>'


def R1_Controle_Clorella(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):

        if column == 'Controle_Clorella':
            r1_controle = (100 - pd.to_numeric(value_df)) / 100
            return r1_controle


def Controle_Clorella(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):

        if column == 'Controle_Clorella':
            r1_controle = (100 - pd.to_numeric(value_df)) / 100
            r2_controle = (r1_controle - r1_controle) / (1 - r1_controle)
            result_controle = np.log10(1 - r2_controle)

            print("controle Chlorella", r1_controle, "r1 controle", r2_controle, "r2 controle", result_controle, "result control", pd.to_numeric(value_df), "valor que chegou")
            return result_controle


def Chlorella(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):

        if column == 'Chlorella':
            metodo_r1controlella = R1_Controle_Clorella(dataframe)
            r1_clor = (100 - pd.to_numeric(value_df)) / 100
            r2_clor = np.nan_to_num((r1_clor - metodo_r1controlella)
                                           / (1 - metodo_r1controlella))
            result_clor = np.nan_to_num(np.log10(1 - r2_clor))

            print("Chlorella", r1_clor, "r1 core",  r2_clor, "r2 core", result_clor, "result control", pd.to_numeric(value_df), "valor que chegou",  metodo_r1controlella, "metodo r1 controle")
            return result_clor


def R1_Controle_CER(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):

        if column == 'Controle_Ceriodaphnia':
            r1_controle = (100 - pd.to_numeric(value_df)) / 100
            return r1_controle


def Controle_CER(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):

        if column == 'Controle_Ceriodaphnia':
            r1_controle = ((100 - pd.to_numeric(value_df)) / 100)
            r2_controle = (r1_controle - r1_controle) / (1 - r1_controle)
            result_controle = np.log10(1 - r2_controle)

            print("Ceriodaphnia controle", r1_controle, "r1 controle", r2_controle, "r2 controle", result_controle, "result control", pd.to_numeric(value_df), "valor que chegou")
            return result_controle


def Ceriodaphnia(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):

        if column == 'Ceriodaphnia':
            r1_cer = ((100 - pd.to_numeric(value_df)) / 100)
            r2_cer = (r1_cer - R1_Controle_CER(dataframe)) / (1 - R1_Controle_CER(dataframe))
            result_cer = (np.log10(1 - r2_cer))

            print("Ceriodaphnia", r1_cer, "r1 cer", r2_cer, "r2 cer", result_cer, "resultado cer", pd.to_numeric(value_df), "valor que chegou", R1_Controle_CER(dataframe), "metodo r1 controle")
            return result_cer


def calculate_ecotox(dataframe):
    for i in range(len(dataframe)):
        print(i)
        print(len(dataframe))

        ceriodaphnia_value = Ceriodaphnia(dataframe)
        chlorella_value = Chlorella(dataframe)

        media_ecotox = np.nan_to_num((ceriodaphnia_value + chlorella_value) / 2)
        dataframe["RISCO_ECOTOX"] = np.nan_to_num(1 - np.power(10, media_ecotox))
        print(media_ecotox, "media ecotox")
        print(dataframe["RISCO_ECOTOX"][0], "resultado final de tudo")

        conditions = [
            (dataframe["RISCO_ECOTOX"] >= 0.76),
            (dataframe["RISCO_ECOTOX"] >= 0.51) & (dataframe["RISCO_ECOTOX"] <= 0.75),
            (dataframe["RISCO_ECOTOX"] >= 0.26) & (dataframe["RISCO_ECOTOX"] <= 0.50),
            (dataframe["RISCO_ECOTOX"] >= 0) & (dataframe["RISCO_ECOTOX"] <= 0.25)
        ]

        classifications = ["Extremo", "Alto", "Moderado", "Baixo"]

        dataframe["Classificacao"] = np.select(conditions, classifications, default=0)

        # Store the final result in session state
        final_result_ecotox = np.mean(dataframe["RISCO_ECOTOX"])
        st.session_state.final_result_ecotox = final_result_ecotox

        return dataframe


def color_classificacao(val):
    color = ''
    if val == 'Baixo':
        color = 'white'
    elif val == 'Moderado':
        color = 'green'
    elif val == 'Alto':
        color = 'yellow'
    elif val == 'Extremo':
        color = 'red'

    return f'background-color: {color}'


def app():
    """
    A página é criada aqui
    """
    st.title("Calcular LOE Ecotox")
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

                df = calculate_ecotox(dataframe)
                st.header("Análise pronta - tabela disponível para download")
                styled_table = df.style.applymap(color_classificacao, subset=['Classificacao'])
                st.write(styled_table.to_html(escape=False), unsafe_allow_html=True)
                st.markdown(download.get_table_download_link(df), unsafe_allow_html=True)

            except (UnicodeDecodeError, ValueError) as e:
                st.error(str(e))
                logger.error(str(e))
                return
        else:
            st.error("Nenhuma tabela foi fornecida. Por favor, forneça uma tabela.")
