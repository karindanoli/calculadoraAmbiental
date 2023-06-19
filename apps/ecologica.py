import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go


st.markdown("Explicação sobre o calculo de evidência ecológica")

# Cria tabela
data = {
"Referencia": [10, 957, 50],
"Ponto 1": [8, 750, 38],
"Ponto 2": [5, 233, 10]
}

df = pd.DataFrame(data, index=["Taxa (No.)", "Indivíduos (No.)", "Microalgas (%)"])


st.table(df)

# Coleta valores da tabela
ref_values = df["Referencia"]
site_a_values = df["Ponto 1"]
site_b_values = df["Ponto 2"]

# divisão do valor da amostra pelo valor de referência.
taxa_a = site_a_values / ref_values
taxa_b = site_b_values / ref_values

# Calcula o log (R1)
log_a = abs(taxa_a.apply(math.log10))
log_b = abs(taxa_b.apply(math.log10))

# Calcula a soma dos logs e multiplicca por -1
result_a = -1 * log_a.sum()
result_b = -1 * log_b.sum()

# calcula o n para a média
num_valores = len(df.columns)

# Finaliza a BKX_Triad
bkx_triad_a = 1 - math.pow(10, (result_a / num_valores))
bkx_triad_b = 1 - math.pow(10, (result_b / num_valores))

# Display the results
results_data = {
"Referencia": [0, 0, 0],
"Ponto 1": [0, result_a, bkx_triad_a],
"Ponto 2": [0, result_b, bkx_triad_b]
}

results_df = pd.DataFrame(results_data, index=["Referencia", "Ponto 1", "Ponto 2"])
st.table(results_df)

# grafico
fig = go.Figure()
for column in results_df.columns:
    fig.add_trace(go.Bar(x=[column], y=[results_df[column][1]], name=column))

fig.update_layout(
    title="Results",
    xaxis_title="Columns",
    yaxis_title="Result",
    width=600,
    height=400
)

st.plotly_chart(fig)