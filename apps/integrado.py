import streamlit as st
import matplotlib.pyplot as plt
import math
import plotly.graph_objects as go



st.title("Análise integrada")
st.markdown("Explicação sobre o calculo de análise integrada")

# Resultados das análises
result_page1 = 0.8
result_page2 = 0.6
result_page3 = 0.7

# Log dos resultados
log_result_page1 = math.log(result_page1)
log_result_page2 = math.log(result_page2)
log_result_page3 = math.log(result_page3)

R1 = 1 - log_result_page1
R2 = 1 - log_result_page2
R3 = 1 - log_result_page3

# Valores fixos vindos de JENSEN & MESMAN, 2006
B = 1.5
C = 2
D = 1

R = (R1 * B + R2 * C + R3 * D) / (B + C + D)

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