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
        "ID": "", "Pontos de Coleta": "", "Controle_NumeroIndividuos": "", "NumeroIndividuos": "",
        "Controle_Cyanobacteria": "", "Cyanobacteria": "",
        "Controle_filamentosas": "", "filamentosas": "", "Controle_diversidade": "", "diversidade": "", "riqueza": ""}

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
    example = pd.DataFrame(columns=["ID", "Pontos de Coleta", "CTE", "PH", "DBO", "Turbidez",
                                    "NT", "PT", "TEMP", "SOLIDOS", "OD"])
    csv = example.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="tabelaTemplate.csv">Download tabelaTemplate.csv</a>'


def R1_NI_Controle(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):

        if column == 'Controle_NumeroIndividuos':
            print("Controle", value_df)
            return pd.to_numeric(value_df)


def Controle_NumeroIndividuos(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):

        if column == 'Controle_NumeroIndividuos':
            r1_NI_controle = R1_NI_Controle(dataframe)
            print(r1_NI_controle, "NumeroIndividuos", value_df)
            result_NI_controle = np.log(r1_NI_controle)

            print(r1_NI_controle, "NumeroIndividuos", result_NI_controle, pd.to_numeric(value_df))
            return result_NI_controle


def NumeroIndividuos(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):

        if column == 'NumeroIndividuos':
            r1_NI = pd.to_numeric(value_df) / R1_NI_Controle(dataframe)
            print(r1_NI, "NumeroIndividuos", value_df)
            result_NI = np.log(r1_NI)

            print(r1_NI, "NumeroIndividuos", result_NI, pd.to_numeric(value_df))
            return result_NI


def R1_CY_Controle(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):

        if column == 'Controle_Cyanobacteria':
            print("Controle", value_df)
            return pd.to_numeric(value_df)


def Controle_Cyanobacteria(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):

        if column == 'Controle_Cyanobacteria':
            r1_CY_controle = R1_CY_Controle(dataframe)
            print(r1_CY_controle, "Controle_Cyanobacteria", value_df)
            result_CY_controle = np.log(r1_CY_controle)

            print(r1_CY_controle, "Controle_Cyanobacteria", result_CY_controle, pd.to_numeric(value_df))
            return result_CY_controle


def Cyanobacteria(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):

        if column == 'Cyanobacteria':
            r1_CY = pd.to_numeric(value_df) / R1_CY_Controle(dataframe)
            print(r1_CY, "Cyanobacteria", value_df)
            result_CY = np.log(r1_CY)

            print(r1_CY, "Cyanobacteria", result_CY, pd.to_numeric(value_df))
            return result_CY


def R1_FI_Controle(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):

        if column == 'Controle_filamentosas':
            print("Controle", value_df)
            return pd.to_numeric(value_df)


def Controle_filamentosas(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):

        if column == 'Controle_filamentosas':
            r1_FI_controle = R1_FI_Controle(dataframe)
            print(r1_FI_controle, "Controle_filamentosas", value_df)
            result_FI_controle = np.log(r1_FI_controle)

            print(r1_FI_controle, "Controle_filamentosas", result_FI_controle, pd.to_numeric(value_df))
            return result_FI_controle


def filamentosas(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):

        if column == 'filamentosas':
            r1_FI = pd.to_numeric(value_df) / R1_FI_Controle(dataframe)
            result_FI = np.log(r1_FI)
            print(r1_FI, "filamentosas", result_FI, pd.to_numeric(value_df))
            return result_FI


def riqueza(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):
        if column == 'riqueza':
            resultado3_riqueza = 1 * (
                    NumeroIndividuos(dataframe) + Cyanobacteria(dataframe) + filamentosas(dataframe)
            )
            # Clip the values to ensure they are positive or above a small epsilon value
            eps = 1e-9
            clipped_resultado3 = np.clip(resultado3_riqueza, eps, None)

            # Calculate result_riqueza without using np.log10
            result_riqueza = 1 - np.log(1 + clipped_resultado3 / 3)
            #                    é log de 10 tem que consertar
            # Replace any invalid values (NaN or infinite) with zero
            result_riqueza = np.nan_to_num(result_riqueza, nan=0, posinf=0, neginf=0)

            result2_riqueza = np.log(1 - result_riqueza)
            if result2_riqueza is not None:
                return result2_riqueza


def R1_DIVER_Controle(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):
        if column == 'Controle_diversidade':
            print("Controle", value_df)
            return pd.to_numeric(value_df)


def Controle_diversidade(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):
        if column == 'Controle_diversidade':
            r1_diversidade = pd.to_numeric(value_df) / R1_DIVER_Controle(dataframe)
            result_diversidade = np.log(r1_diversidade)
            print(r1_diversidade, "Controle_diversidade", result_diversidade, pd.to_numeric(value_df))
            if result_diversidade is not None:
                return result_diversidade


def diversidade(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):
        if column == 'diversidade':
            r1_diversidade = pd.to_numeric(value_df) / R1_DIVER_Controle(dataframe)
            print(r1_diversidade, "diversidade", value_df)
            r5_diversidade = 1 - np.power(10, -r1_diversidade)
            result_diversidade = np.log(1 - r5_diversidade)
            print(r1_diversidade, "diversidade", result_diversidade, pd.to_numeric(value_df))
            if result_diversidade is not None:
                return result_diversidade


def risco_ecologico(dataframe):
    for i in range(len(dataframe)):
        diversidade_result = diversidade(dataframe)
        riqueza_result = riqueza(dataframe)

        if diversidade_result is not None and riqueza_result is not None:
            dataframe["RISCO_ECO"] = 1 - np.power(10, (diversidade_result + riqueza_result) / 2)
            print(dataframe["RISCO_ECO"][0])
        else:
            dataframe["RISCO_ECO"] = 0  # Set a default value when the result is None
            print(dataframe["RISCO_ECO"][0])

            return dataframe["RISCO_ECO"]


def calculate_eco(dataframe):
    for i in range(len(dataframe)):
        print(i)
        print(len(dataframe))

        diversidade_result = diversidade(dataframe)
        riqueza_result = riqueza(dataframe)

        if diversidade_result is not None and riqueza_result is not None:
            dataframe["RISCO_ECO"] = 1 - np.power(10, (diversidade_result + riqueza_result) / 2)
            print(dataframe["RISCO_ECO"][0])
        else:
            dataframe["RISCO_ECO"] = 0  # Set a default value when the result is None
            print(dataframe["RISCO_ECO"][0])

        conditions = [
            (dataframe["RISCO_ECO"] >= 91) & (dataframe["RISCO_ECO"] <= 100),
            (dataframe["RISCO_ECO"] >= 71) & (dataframe["RISCO_ECO"] <= 90),
            (dataframe["RISCO_ECO"] >= 51) & (dataframe["RISCO_ECO"] <= 70),
            (dataframe["RISCO_ECO"] >= 26) & (dataframe["RISCO_ECO"] <= 50),
            (dataframe["RISCO_ECO"] >= 0) & (dataframe["RISCO_ECO"] <= 25)
        ]

        classifications = ["Otima", "Boa", "Razoavel", "Ruim", "Pessimo"]

        dataframe["Classificacao"] = np.select(conditions, classifications, default=0)

        final_result_eco = np.mean(dataframe["RISCO_ECO"])
        st.session_state.final_result_eco = final_result_eco

        return dataframe


def color_classificacao(val):
    color = ''
    if val == 'Otima':
        color = 'blue'
    elif val == 'Boa':
        color = 'green'
    elif val == 'Razoavel':
        color = 'yellow'
    elif val == 'Ruim':
        color = 'red'
    elif val == 'Pessimo':
        color = 'black'

    return f'background-color: {color}'


def app():
    """
    A página é criada aqui
    """
    st.title("Calcular IQA")
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
