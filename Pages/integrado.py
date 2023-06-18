import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math


def AnaliseIntegrada():

    # Set the title and markdown text for the page
    st.title("Evidência ecológico integrado")
    st.markdown("coisas de evidência ecológica")

    # Retrieve the results from the different pages
    result_page1 = 0.8  # Replace with the actual result from page 1
    result_page2 = 0.6  # Replace with the actual result from page 2
    result_page3 = 0.7  # Replace with the actual result from page 3

    # Perform the calculations
    log_result_page1 = math.log(result_page1)
    R1 = 1 - log_result_page1
    R2 = 1 - result_page2
    R3 = 1 - result_page3

    B = 1.5
    C = 2
    D = 1

    R = (R1 * B + R2 * C + R3 * D) / (B + C + D)

    # Determine the risk category based on the result
    risk_category = ""
    if 0 <= R <= 0.25:
        risk_category = "Low risk"
    elif 0.25 < R <= 0.5:
        risk_category = "Moderate risk"
    elif 0.5 < R <= 0.75:
        risk_category = "High risk"
    elif R > 0.75:
        risk_category = "Too much risk"

    # Display the result
    st.subheader("Result")
    st.text(f"R = {R:.2f}")
    st.text("Risk Category: " + risk_category)

    # Create the gauge graphic
    fig, ax = plt.subplots()

    # Define the gauge range and colors
    gauge_range = [0, 0.25, 0.5, 0.75, 1]
    colors = ["green", "yellowgreen", "orange", "red"]

    # Create the gauge sectors
    for i in range(len(gauge_range) - 1):
        start_angle = 90 - (gauge_range[i] * 180)
        end_angle = 90 - (gauge_range[i + 1] * 180)
        sector = plt.Wedge((0.5, 0.5), 0.4, start_angle, end_angle, width=0.2, facecolor=colors[i])
        ax.add_patch(sector)

    # Add the needle to indicate the result
    needle_angle = 90 - (R * 180)
    needle = plt.Wedge((0.5, 0.5), 0.2, needle_angle, needle_angle, width=0.02, facecolor="black")
    ax.add_patch(needle)

    # Set the aspect ratio and remove axis
    ax.set(aspect="equal")
    ax.axis("off")

    # Display the gauge graphic
    st.pyplot(fig)

    # Display additional information
    st.markdown("""
    The calculation is performed by retrieving the results from the different pages and applying the specified formula. The resulting value, R, is then categorized into different risk levels based on the specified ranges.
    """)