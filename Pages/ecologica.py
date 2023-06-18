import streamlit as st
import pandas as pd
import math


def AnaliseEcologica():
        # Set the title and markdown text for the page
        st.markdown("Explicação sobre o calculo de evidência ecológica")

        # Create a table with the example data
        data = {
        "Reference": [10, 957, 50],
        "Site A": [8, 750, 38],
        "Site B": [5, 233, 10]
        }

        df = pd.DataFrame(data, index=["Taxa (No.)", "Individuals (No.)", "Herbivores (%)"])


        st.table(df)

        # Perform the calculations
        ref_values = df["Reference"]
        site_a_values = df["Site A"]
        site_b_values = df["Site B"]

        # Step 1: Ratio between site x and reference
        ratio_a = site_a_values / ref_values
        ratio_b = site_b_values / ref_values

        # Step 2: Calculate absolute values of log (R1)
        log_ratio_a = abs(ratio_a.apply(math.log10))
        log_ratio_b = abs(ratio_b.apply(math.log10))

        # Step 3: Calculate sum of all values and multiply with -1
        result_a = -1 * log_ratio_a.sum()
        result_b = -1 * log_ratio_b.sum()

        # Step 4: Calculate number of endpoints
        num_endpoints = len(df.columns)

        # Step 5: Use results from step 3 and 4 in the BKX_Triad formula
        bkx_triad_a = 1 - math.pow(10, (result_a / num_endpoints))
        bkx_triad_b = 1 - math.pow(10, (result_b / num_endpoints))

        # Display the results
        results_data = {
        "Reference": [0, 0, 0],
        "Site A": [0, result_a, bkx_triad_a],
        "Site B": [0, result_b, bkx_triad_b]
        }

        results_df = pd.DataFrame(results_data, index=["Results (R3)", "Results (R4)", "Results (R5)"])
        st.table(results_df)
