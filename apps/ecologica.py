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
    st.write("Preencha todos os campos, o cálculo IQA só será correto com todos os valores")
    st.write("Use somente valores alfanuméricos (A-Z,0-9)")

    if 'reset_key' not in st.session_state:
        st.session_state.reset_key = 0

    default_values = {
        "ID": "", "Pontos de Coleta": "", "BPS": "", "BPA": "", "Dietilftalato": "", "Benzofenona": ""}

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

def BPS(dataframe, dtype=np.complex):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):
        total_mult = 1
        if column == 'BPS':
            =np.abs(1 / (1 + np.power(((LOG($C4) - LOG(C3)) / 0, 4)))
            qi_CTE = np.abs(-8.723 * np.log(pd.to_numeric(value_df)) + 88.714)
            iqa_CTE = np.power(qi_CTE, 0.15)
            total_mult *= iqa_CTE
            print(qi_CTE, "BPS", iqa_CTE, total_mult, pd.to_numeric(value_df))
            return total_mult

def BPA(dataframe):
    for column, value_df in zip(dataframe.columns, dataframe.values.T):
        total_mult = 1
        if column == 'BPA':
            qi_PH = 93 * np.exp(-(((pd.to_numeric(value_df) - 7.5) ** 2) / 2 * (0.652 ** 2)))
            iqa_PH = np.power(qi_PH, 0.12)
            total_mult = total_mult * iqa_PH
            print(qi_PH, "BPA", iqa_PH, total_mult, pd.to_numeric(value_df))
            return total_mult

def Dietilftalato(dataframe):
  for column, value_df in zip(dataframe.columns, dataframe.values.T):
                total_mult = 1
                if column == 'Dietilftalato':
                    qi_DBO = -30.1 * np.log(pd.to_numeric(value_df)) + 103.45
                    # qi_DBO = 2
                    iqa_DBO = np.power(qi_DBO, 0.1)
                    total_mult = total_mult * iqa_DBO
                    print(qi_DBO,"Dietilftalato", iqa_DBO, total_mult,pd.to_numeric(value_df))
                    return total_mult

def Benzofenona(dataframe):
      for column, value_df in zip(dataframe.columns, dataframe.values.T):
            total_mult = 1
            if column == 'Benzofenona':
                qi_Turbidez = -26.45 * np.log(pd.to_numeric(value_df)) + 136.37
                iqa_Turbidez = qi_Turbidez ** 0.08
                total_mult = total_mult * iqa_Turbidez
                print(qi_Turbidez,"Benzofenona", iqa_Turbidez, total_mult,pd.to_numeric(value_df))
                return total_mult


def calculate_eco(dataframe):

    for i in range(len(dataframe)):
        # total_mult = 1
        print(i)
        print(len(dataframe))


        dataframe["IQA"] = CTE(dataframe)*PH(dataframe)*DBO(dataframe)*OD(dataframe)*SOLIDOS(dataframe)*TEMP(dataframe)*PT(dataframe)*NT(dataframe)*Turbidez(dataframe)
        print(dataframe["IQA"][0])
        print(CTE(dataframe))

        conditions = [
            (dataframe["IQA"] >= 91) & (dataframe["IQA"] <= 100),
            (dataframe["IQA"] >= 71) & (dataframe["IQA"] <= 90),
            (dataframe["IQA"] >= 51) & (dataframe["IQA"] <= 70),
            (dataframe["IQA"] >= 26) & (dataframe["IQA"] <= 50),
            (dataframe["IQA"] >= 0) & (dataframe["IQA"] <= 25)
        ]

        classifications = ["Otima", "Boa", "Razoavel", "Ruim", "Pessimo"]

        dataframe["Classificacao"] = np.select(conditions, classifications, default=0)

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