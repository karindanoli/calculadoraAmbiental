import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def load_data():
    """
    Carrega os dados de ocorrências aeronáuticas do CENIPA.

    :return: DataFrame com colunas selecionadas.
    """
    columns = {'X': 'latitude',
               'Y': 'longitude',
               'OBJECTID': 'ID',
               'codigo': 'codigo',
               'uf': 'uf',
               'codigo_anterior': 'versao anterior',
               'regime': 'regime',
               'enquadramento': 'enquadramento',
               'responsavel': 'orgao_responsavel',
               'latitude': 'latitude',
               'longitude': 'longitude',
               'corpo_hidrico': 'nome do rio',
               'Ano_1': 'ano',
               'Cont_1': 'contagem',
               'Media_1': 'media',
               'Min_1': 'minimo',
               'Max_1': 'maximo',
               'Stddev_1': 'stddev',
               'Variance_1': 'variancia'}

    data = pd.read_csv('IQA2017.csv')
    data = data.rename(columns=columns)

    data = data[list(columns.values())]

    return data


# carregar os dados
df = load_data()
labels = df.uf.unique().tolist()


# SIDEBAR
# Parâmetros e número de ocorrências
st.sidebar.header("Parâmetros")
info_sidebar = st.sidebar.empty()    # placeholder, para informações filtradas que só serão carregadas depois

# Slider de seleção do ano
st.sidebar.subheader("Ano")
year_to_filter = st.sidebar.slider('Escolha o ano desejado', 2008, 2018, 2017)

# Checkbox da Tabela
st.sidebar.subheader("Tabela")
tabela = st.sidebar.empty()    # placeholder que só vai ser carregado com o df_filtered

# Multiselect com os lables únicos dos tipos de classificação
label_to_filter = st.sidebar.multiselect(
    label="Escolha o Estado",
    options=labels,
    default=["RJ", 'MG','MS','DF','SE','PR','CE','RN','MT','ES','PE','PB','BA']
)

# Informação no rodapé da Sidebar
st.sidebar.markdown("""
A base de dados de ocorrências aeronáuticas é gerenciada pelo ***Centro de Investigação e Prevenção de Acidentes 
Aeronáuticos (CENIPA)***.
""")

# Somente aqui os dados filtrados por ano são atualizados em novo dataframe
filtered_df = df.uf.isin(label_to_filter)

# Aqui o placehoder vazio finalmente é atualizado com dados do filtered_df
info_sidebar.info("{} ocorrências selecionadas.".format(filtered_df.shape[0]))




# MAIN
st.title("CENIPA - Acidentes Aeronáuticos")
st.markdown(f"""
            ℹ️ Estão sendo exibidas as ocorrências classificadas como **{", ".join(label_to_filter)}**
            para o ano de **{year_to_filter}**.
            """)

# raw data (tabela) dependente do checkbox
if tabela.checkbox("Mostrar tabela de dados"):
    st.write(filtered_df)

plt.figure(figsize=(15, 5))
plt.hist(df.uf, bins=30, rwidth=.8)
plt.grid()
st.pyplot(plt)
plt.clf()



