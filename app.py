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
# Load Custom CSS
# =====================================================

def load_css():
    with open("style.css", encoding="utf-8") as css:
        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )


# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="AI Data Analyst Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()


# =====================================================
# Sidebar
# =====================================================

with st.sidebar:

    st.markdown("""
# 🤖 AI Data Analyst

### Powered by Gemini AI
""")

    st.markdown("---")

    menu = st.radio(
        "Navigation",
        [
            "🤖 AI Chat",
            "📊 Dashboard",
            "📈 Visualizations",
            "🧹 Data Cleaning",
            "💡 AI Insights",
            "📄 Report"
        ]
    )

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload CSV Dataset",
        type=["csv"]
    )

    if uploaded_file is not None:

        st.markdown("---")

        st.subheader("📁 Dataset")

        st.write(uploaded_file.name)

        st.write(f"Size : {uploaded_file.size/1024:.2f} KB")


# =====================================================
# Hero Section
# =====================================================

st.markdown("""
<h1 style="text-align:center;">
🤖 AI Data Analyst Agent
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style="
text-align:center;
font-size:20px;
margin-top:-10px;">
Analyze • Visualize • Clean • Chat • Report
</p>
""", unsafe_allow_html=True)

st.write("")

# =====================================================
# Feature Cards
# =====================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.info("📊 **Dashboard**\n\nView dataset statistics and KPIs.")

with c2:
    st.info("📈 **Visualizations**\n\nGenerate interactive charts.")

with c3:
    st.info("🧹 **Data Cleaning**\n\nHandle missing values and duplicates.")

c4, c5, c6 = st.columns(3)

with c4:
    st.info("🤖 **AI Chat**\n\nAsk questions about your data.")

with c5:
    st.info("💡 **AI Insights**\n\nGenerate smart insights.")

with c6:
    st.info("📄 **PDF Report**\n\nDownload a professional report.")

st.divider()

# =====================================================
# AI Chat (Available Before Upload)
# =====================================================

if menu == "🤖 AI Chat":

    st.header("🤖 AI Data Analyst")

    question = st.text_area(
        "Ask a question",
        height=140,
        placeholder="Example: Which column has the highest missing values?"
    )

    if uploaded_file is None:

        st.warning("Please upload a CSV dataset first to enable AI analysis.")

    else:

        df = pd.read_csv(uploaded_file)

        if st.button("Ask AI", width="stretch"):

            if question.strip():

                with st.spinner("Analyzing dataset..."):

                    answer = ask_agent(question, df)

                st.chat_message("user").write(question)

                st.chat_message("assistant").write(answer)

            else:

                st.warning("Please enter a question.")

# =====================================================
# Stop if Dataset Not Uploaded
# =====================================================

if uploaded_file is None:

    st.stop()

# =====================================================
# Load Dataset
# =====================================================

df = pd.read_csv(uploaded_file)

st.success("✅ Dataset loaded successfully.")

st.write("")
# =====================================================
# Navigation
# =====================================================

if menu == "📊 Dashboard":

    st.header("📊 Dashboard")

    show_overview(df)


# =====================================================
# Visualizations
# =====================================================

elif menu == "📈 Visualizations":

    st.header("📈 Interactive Visualizations")

    st.write("Explore your dataset using interactive charts.")

    show_visualizations(df)


# =====================================================
# Data Cleaning
# =====================================================

elif menu == "🧹 Data Cleaning":

    st.header("🧹 Data Cleaning")

    st.write("Clean your dataset before analysis.")

    show_cleaning(df)


# =====================================================
# AI Insights
# =====================================================

elif menu == "💡 AI Insights":

    st.header("💡 AI Insights")

    st.write("Automatically generated insights from your dataset.")

    show_ai_insights(df)


# =====================================================
# Report
# =====================================================

elif menu == "📄 Report":

    st.header("📄 AI Report Generator")

    st.success("""
Your report includes:

✅ Dataset Summary

✅ Missing Value Analysis

✅ Statistical Summary

✅ AI Generated Insights

✅ Recommendations
""")

    insights = generate_insights(df)

    if st.button("📄 Generate PDF Report", width="stretch"):

        with st.spinner("Generating Report..."):

            filename = generate_report(df, insights)

        st.success("Report Generated Successfully!")

        with open(filename, "rb") as pdf:

            st.download_button(
                "⬇ Download PDF Report",
                data=pdf,
                file_name=filename,
                mime="application/pdf",
                width="stretch"
            )


# =====================================================
# Dataset Preview
# =====================================================

st.divider()

st.subheader("📂 Dataset Preview")

st.dataframe(
    df.head(10),
    width="stretch"
)


# =====================================================
# Dataset Information
# =====================================================

st.subheader("📋 Dataset Information")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Rows", len(df))

with c2:
    st.metric("Columns", len(df.columns))

with c3:
    st.metric("Missing Values", int(df.isnull().sum().sum()))

with c4:
    st.metric("Duplicates", int(df.duplicated().sum()))


# =====================================================
# Footer
# =====================================================

st.divider()

st.markdown(
"""
<div style='text-align:center;'>

<h3>🤖 AI Data Analyst Agent</h3>

<p>
Built with ❤️ by <b>Aswitha S</b>
</p>

<p>
Powered by Streamlit • Gemini AI • Plotly • Pandas
</p>

</div>
""",
unsafe_allow_html=True
)