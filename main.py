import streamlit as st
from streamlit_option_menu import option_menu
from apps import home, iqa
from loguru import logger
from pathlib import Path

st.set_page_config(page_title="MODV AMBIENTAL", layout="wide")
enable_logging = False

if enable_logging:
    logname = "file_1.log"
    logger.add(logname)
    lines = "\n".join(Path(logname).read_text().splitlines()[-10:])
    st.code(lines)

apps = [
    {"func": home.app, "title": "Home", "icon": "house"},
    {"func": iqa.app, "title": "Calcular IQA", "icon": "calculator"},
    {"func": integrado.app, "title": "Integrado", "icon": "house"},
    {"func": mapa.app, "title": "Mapa", "icon": "calculator"},
    {"func": ecologica.app, "title": "Ecologica", "icon": "calculator"},
    {"func": previsaoIqa.app, "title": "previsaoIqa", "icon": "house"},
]

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        "Menu Principal",
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
    )

    st.sidebar.title("Sobre")
    st.sidebar.info(
        """
         O Índice de Qualidade de Água (IQA) médio anual de um ponto de monitoramento é calculado a partir da média
         dos valores do índice obtidos nas medições realizadas naquele ponto durante o ano. Os valores de IQA calculados
         correspondem aos dados das próprias entidades responsáveis pelo monitoramento nas Unidades da Federação,
         em virtude das variações entre as fórmulas utilizadas para o cálculo, com o intuito de uniformizar a forma de
         cálculo do IQA e tornar os valores comparáveis para todo o território nacional    
 
        Desenvolvido por Karin de Oliveira e Bruno de Oliveira
 
        Código fonte: <https://github.com/karindanoli/NewVersion_Modv>
 
        Ícones do Menu: <https://icons.getbootstrap.com>
    """
    )

for app in apps:

    if app["title"] == selected:
        app["func"]()
        break
