import streamlit as st
import pandas as pd

from dashboard import (
    show_overview,
    show_visualizations,
    show_cleaning,
    show_ai_insights
)

from agent import ask_agent
from report import generate_report
from insights import generate_insights


# =====================================================
# Load CSS
# =====================================================

def load_css():
    with open("style.css") as css:
        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )


# =====================================================
# Page Config
# =====================================================

st.set_page_config(
    page_title="AI Data Analyst Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()


# =====================================================
# Sidebar
# =====================================================

with st.sidebar:

    st.title("AI Data Analyst")

    st.caption("Powered by Gemini AI")

    st.markdown("---")

    menu = st.radio(
        "Navigation",
        (
            "AI Chat",
            "Dashboard",
            "Visualizations",
            "Data Cleaning",
            "AI Insights",
            "Report"
        )
    )

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload CSV Dataset",
        type=["csv"]
    )

    # Dataset Information
    if uploaded_file is not None:

        st.markdown("---")

        st.subheader("Dataset")

        st.write(f"**Name:** {uploaded_file.name}")

        size = uploaded_file.size / 1024

        st.write(f"**Size:** {size:.2f} KB")


# ==========================================
# Main Title
# ==========================================

st.markdown("""
<h1 style="
font-size:60px;
font-weight:800;
color:#2F3E75;
margin-bottom:10px;
font-family:'Outfit',sans-serif;">
AI Data Analyst Agent
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style="
font-size:24px;
color:#5B6475;
font-family:'Outfit',sans-serif;
margin-bottom:30px;">
Analyze datasets using AI-powered insights,
interactive visualizations, automated data cleaning,
and intelligent reporting.
</p>
""", unsafe_allow_html=True)

# =====================================================
# No Dataset
# =====================================================

if uploaded_file is None:

    st.info("Please upload a CSV dataset from the sidebar.")

    st.stop()


# =====================================================
# Read Dataset
# =====================================================

df = pd.read_csv(uploaded_file)

st.success("Dataset loaded successfully.")

st.write("")

# =====================================================
# Navigation
# =====================================================

if menu == "AI Chat":

    st.header("AI Chat")

    question = st.text_area(
        "Ask a question",
        height=140,
        placeholder="Example: Which column has the highest missing values?"
    )

    if st.button("Ask AI", use_container_width=True):

        if question.strip():

            with st.spinner("Analyzing dataset..."):

                answer = ask_agent(question, df)

            st.success("Analysis Completed")

            st.markdown(answer)

        else:

            st.warning("Please enter a question.")


elif menu == "Dashboard":

    show_overview(df)


elif menu == "Visualizations":

    show_visualizations(df)


elif menu == "Data Cleaning":

    show_cleaning(df)


elif menu == "AI Insights":

    show_ai_insights(df)


elif menu == "Report":

    st.header("AI Report")

    st.write(
        "Generate a professional PDF report with dataset statistics and AI-generated insights."
    )

    insights = generate_insights(df)

    if st.button("Generate PDF Report", use_container_width=True):

        filename = generate_report(df, insights)

        with open(filename, "rb") as pdf:

            st.download_button(
                label="Download PDF Report",
                data=pdf,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True
            )