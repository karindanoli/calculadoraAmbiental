import numpy as np
import plotly.graph_objects as go
import streamlit as st

from apps.ecologica import risco_ecologico
from apps.quimica import risco_quimico


# from streamlit.report_thread import get_report_ctx
# from streamlit_cache import cache


# def get_session_state():
#     ctx = get_report_ctx()
#     this_session = st.server.server.Server.get_current()._get_session_info(ctx.session_id).session
#     return this_session
#
# def set_session_state(key, value):
#     this_session = get_session_state()
#     this_session.session_state[key] = value
#
# def get_saved_session_state(key):
#     this_session = get_session_state()
#     return this_session.session_state.get(key, None)

def results(dataframe):
    # Resultados das análises
    result_page1 = risco_ecologico(dataframe)
    return result_page1


def results2(dataframe):
    result_page2 = risco_quimico(dataframe)
    return result_page2


def app():
    st.title("Análise integrada")
    st.markdown("Explicação sobre o calculo de análise integrada")

    print(results)
    print(results2)

    # TODO valor placeholder. Consertar erro onde se user n tem dataframe, causa erro
    # Log dos resultados
    log_result_page1 = np.log10(2 - 1)

    R1 = 1 - log_result_page1

    log_result_page2 = np.log10(2 - 1)
    R2 = 1 - log_result_page2

    # Valores fixos vindos de JENSEN & MESMAN, 2006
    B = 1.5
    C = 2

    R = (R1 * B + R2 * C) / (B + C)

    # Categorias de risco
    risk_category = ""
    if 0 <= R <= 0.25:
        risk_category = "Risco baixo"
    elif 0.25 < R <= 0.5:
        risk_category = "Risco moderado"
    elif 0.5 < R <= 0.75:
        risk_category = "Risco alto"
    elif R > 0.75:
        risk_category = "Risco altissímo"

    # Resultado
    st.subheader("Result")
    st.text(f"R = {R:.2f}")
    st.text("Risk Category: " + risk_category)

    # Grafico gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=R,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 1]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 0.25], 'color': 'green'},
                {'range': [0.25, 0.5], 'color': 'yellow'},
                {'range': [0.5, 0.75], 'color': 'orange'},
                {'range': [0.75, 1], 'color': 'red'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': R
            }
        }
    ))

    fig.update_layout(
        title_text="Risk Level",
        width=400,
        height=300,
    )

    st.plotly_chart(fig)

    # legenda
    st.markdown("""O cálculo é baseado na análise integrada da ARE, onde R é o resultado. Os niveís de risco:""")
    st.markdown("""0 <= R <= 0.25 - Risco baixo - verde""")
    st.markdown("""0.25 < R <= 0.5 - Risco moderado - amarelo""")
    st.markdown("""0.5 < R <= 0.75 - Risco alto - laranja""")
    st.markdown("""R > 0.75 - Risco altissímo - vermelho""")
