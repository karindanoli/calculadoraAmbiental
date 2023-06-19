import base64
import os
import tempfile
import uuid
from typing import Dict, Any

import numpy as np
import pandas as pd
import streamlit as st
from loguru import logger


def save_uploaded_file(file_content, file_name):
    """
    Salva o arquivo que foi subido para um diretório temporário
    """

    _, file_extension = os.path.splitext(file_name)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(tempfile.gettempdir(), f"{file_id}{file_extension}")

    with open(file_path, "wb") as file:
        file.write(file_content.getbuffer())

    return file_path


def download_template():
    example = pd.DataFrame(columns=["ID", "Pontos de Coleta", "pH", "OD(mg/L)", "CE(uS/cm2)", "Turbidez(NTU)",
                                    "Temp.liq(Celsius)", "ORP(mV)", "STD(g/L)", "Salinidade", "DQO(mg/L)", "DBO(mg/L)",
                                    "Fosforo(mg/L)", "Amonia(mg/L)", "Nitrato(mg/L)", "CT(NMP/100mL)", "CTE(NMP/100mL)"
                                    ])
    csv = example.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="tabelaTemplate.csv">Download tabelaTemplate.csv</a>'


def create_table():
    st.subheader("Complete a tabela abaixo:")
    st.write("Valores de coluna são separados por vírgula "
             "(E.g: se preencher o ID com os valores 1,2, "
             "a tabela terá o valor 1 na col 1 e 2 na col 2)")
    st.write("ATENÇÃO: Não coloque espaço entre vírgulas(E.g: 1, 2)")
    st.write("Preencha todos os campos, o cálculo IQA só será correto com todos os valores")
    st.write("Use somente valores alfanuméricos (A-Z,0-9)")

    if 'reset_key' not in st.session_state:
        st.session_state.reset_key = 0

    default_values = {
        "ID": "", "Pontos de Coleta": "", "pH": "", "OD(mg/L)": "", "CE(uS/cm2)": "",
        "Turbidez(NTU)": "", "Temp.liq(Celsius)": "", "ORP(mV)": "", "STD(g/L)": "",
        "Salinidade": "", "DQO(mg/L)": "", "DBO(mg/L)": "", "Fosforo(mg/L)": "",
        "Amonia(mg/L)": "", "Nitrato(mg/L)": "", "CT(NMP/100mL)": "", "CTE(NMP/100mL)": ""
    }

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
    else:
        st.write("Preencha a tabela e clique em 'Criar tabela' para visualizar os dados. ")

    if clear_table_button:
        st.session_state.reset_key += 1
        st.experimental_rerun()


def calculate_iqa(df):
    """
    O cálculo do IQA é feito aqui. Também é aqui que as colunas IQA e Classificacao são adicionadas.
    A classificação depende da pontuação IQA
    """

    # Placeholder for the actual IQA calculation
    # Add your calculation logic here
    iqa = 0
    df["IQA"] = iqa
    # Add "Classificacao" based on the IQA score
    df["Classificacao"] = ""

    conditions = [
        (df["IQA"] >= 91) & (df["IQA"] <= 100),
        (df["IQA"] >= 71) & (df["IQA"] <= 90),
        (df["IQA"] >= 51) & (df["IQA"] <= 70),
        (df["IQA"] >= 26) & (df["IQA"] <= 50),
        (df["IQA"] >= 0) & (df["IQA"] <= 25)
    ]

    classifications = ["Otima", "Boa", "Razoavel", "Ruim", "Pessimo"]

    df["Classificacao"] = np.select(conditions, classifications, default=0)

    return df


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


def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="resultados.csv">Download resultados.csv</a>'


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
                    file_path = save_uploaded_file(file_uploader, file_uploader.name)
                    df = pd.read_csv(file_path, encoding='utf-8')
                    logger.info("data", df)
                elif url_input:
                    file_path = url_input
                    df = pd.read_csv(file_path, encoding='utf-8')
                    logger.info("url", df)
                elif user_created_table is not None:
                    df = user_created_table
                    logger.info("user created", df)
                else:
                    raise ValueError("Nenhuma tabela foi fornecida.")

                df = calculate_iqa(df)
                st.header("Análise IQA pronta - tabela disponível para download")
                styled_table = df.style.applymap(color_classificacao, subset=['Classificacao'])
                st.write(styled_table.to_html(escape=False), unsafe_allow_html=True)
                st.markdown(get_table_download_link(df), unsafe_allow_html=True)

            except (UnicodeDecodeError, ValueError) as e:
                st.error(str(e))
                logger.error(str(e))
                return
        else:
            st.error("Nenhuma tabela foi fornecida. Por favor, forneça uma tabela.")
