import streamlit as st
from streamlit_option_menu import option_menu

from apps import home, iqa, integrado, quimica, ecotox, ecologica, previsaoIqa

apps = [
    {"func": home.app, "title": "Home"},
    {"func": iqa.app, "title": "Calcular LOE IQA"},
    {"func": integrado.app, "title": "Integrado"},
    # {"func": mapa.app, "title": "Mapa", "icon": "calculator"},
    {"func": quimica.app, "title": "Calcular LOE Quimica"},
    {"func": ecotox.app, "title": "Calcular LOE Ecotox"},
    {"func": ecologica.app, "title": "Calcular LOE Ecologica"},
    {"func": previsaoIqa.app, "title": "previsaoIqa"},
]

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        "Menu Principal",
        options=titles
    )

    st.sidebar.title("Sobre")
    st.sidebar.info(
        """
         O Índice de Qualidade de Água (IQA) médio anual de um ponto de monitoramento é calculado a partir da média
         dos valores do índice obtidos nas medições realizadas naquele ponto durante o ano. Os valores de IQA calculados
         correspondem aos dados das próprias entidades responsáveis pelo monitoramento nas Unidades da Federação,
         em virtude das variações entre as fórmulas utilizadas para o cálculo, com o intuito de uniformizar a forma de
         cálculo do IQA e tornar os valores comparáveis para todo o território nacional    
 
        Desenvolvido por Karin de Oliveira
 
        Código fonte: <https://github.com/karindanoli/NewVersion_Modv>
 
        Ícones do Menu: <https://icons.getbootstrap.com>
    """
    )

for app in apps:

    if app["title"] == selected:
        app["func"]()
        break
