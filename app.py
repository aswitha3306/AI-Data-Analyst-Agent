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
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="AI Data Analyst Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# Load CSS
# =====================================================

def load_css():
    with open("style.css", encoding="utf-8") as css:
        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# =====================================================
# Sidebar
# =====================================================

with st.sidebar:

    st.title("🤖 AI Data Analyst")
    st.caption("Powered by Gemini AI")

    st.divider()

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

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload CSV Dataset",
        type=["csv"]
    )

    if uploaded_file is not None:

        st.divider()

        st.subheader("📁 Dataset")

        st.write(f"**Name:** {uploaded_file.name}")

        st.write(f"**Size:** {uploaded_file.size/1024:.2f} KB")

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
font-size:22px;
color:#666;">
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
# Load Dataset (FIXED)
# =====================================================

if uploaded_file is None:
    st.info("👈 Upload a CSV file from the sidebar to get started.")
    st.stop()

@st.cache_data
def load_data(file):
    file.seek(0)
    return pd.read_csv(file)

try:
    df = load_data(uploaded_file)
    st.success("✅ Dataset loaded successfully!")
except Exception as e:
    st.error(f"Unable to read CSV: {e}")
    st.stop()
# =====================================================
# Navigation
# =====================================================

if menu == "🤖 AI Chat":

    st.header("🤖 AI Data Analyst")

    st.write("Ask questions about the uploaded dataset using Gemini AI.")

    question = st.text_area(
        "Ask a question",
        height=150,
        placeholder="Example: Which column has the highest missing values?"
    )

    if st.button("🚀 Ask AI", width="stretch"):

        if question.strip():

            with st.spinner("Analyzing dataset..."):

                answer = ask_agent(question, df)

            st.chat_message("user").write(question)

            st.chat_message("assistant").write(answer)

        else:

            st.warning("Please enter a question.")


# =====================================================
# Dashboard
# =====================================================

elif menu == "📊 Dashboard":

    st.header("📊 Dashboard")

    show_overview(df)


# =====================================================
# Visualizations
# =====================================================

elif menu == "📈 Visualizations":

    st.header("📈 Interactive Visualizations")

    st.write(
        "Explore the dataset using interactive charts."
    )

    show_visualizations(df)


# =====================================================
# Data Cleaning
# =====================================================

elif menu == "🧹 Data Cleaning":

    st.header("🧹 Data Cleaning")

    st.write(
        "Clean missing values, duplicates and prepare the dataset."
    )

    show_cleaning(df)


# =====================================================
# AI Insights
# =====================================================

elif menu == "💡 AI Insights":

    st.header("💡 AI Insights")

    st.write(
        "Automatically generated AI insights from your dataset."
    )

    show_ai_insights(df)


# =====================================================
# Report
# =====================================================

elif menu == "📄 Report":

    st.header("📄 AI Report Generator")

    st.info(
        """
### Your report includes

- Dataset Summary
- Missing Value Analysis
- Statistical Summary
- AI Insights
- Recommendations
"""
    )

    insights = generate_insights(df)

    if st.button("📄 Generate PDF Report", width="stretch"):

        with st.spinner("Generating PDF..."):

            filename = generate_report(df, insights)

        st.success("Report generated successfully!")

        with open(filename, "rb") as pdf:

            st.download_button(
                "⬇ Download PDF",
                pdf,
                file_name=filename,
                mime="application/pdf",
                width="stretch"
            )
# =====================================================
# Dataset Preview
# =====================================================

st.divider()

st.header("📂 Dataset Preview")

st.write("Preview of the first 10 rows of the uploaded dataset.")

st.dataframe(
    df.head(10),
    width="stretch",
    hide_index=True
)


# =====================================================
# Dataset Statistics
# =====================================================

st.divider()

st.header("📊 Dataset Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Rows",
        f"{df.shape[0]:,}"
    )

with col2:
    st.metric(
        "Columns",
        df.shape[1]
    )

with col3:
    st.metric(
        "Missing Values",
        int(df.isnull().sum().sum())
    )

with col4:
    st.metric(
        "Duplicate Rows",
        int(df.duplicated().sum())
    )


# =====================================================
# Column Information
# =====================================================

st.divider()

st.header("📋 Column Information")

column_info = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str),
    "Missing Values": df.isnull().sum().values,
    "Unique Values": df.nunique().values
})

st.dataframe(
    column_info,
    width="stretch",
    hide_index=True
)


# =====================================================
# Numerical Summary
# =====================================================

numeric_df = df.select_dtypes(include="number")

if not numeric_df.empty:

    st.divider()

    st.header("📈 Statistical Summary")

    st.dataframe(
        numeric_df.describe().T,
        width="stretch"
    )


# =====================================================
# Footer
# =====================================================

st.divider()

st.markdown(
"""
<div style="text-align:center;padding:25px;">

<h3 style="color:#4F46E5;">
🤖 AI Data Analyst Agent
</h3>

<p style="font-size:18px;">
Built with ❤️ by <b>Aswitha S</b>
</p>

<p style="color:gray;">
Powered by Streamlit • Gemini AI • Pandas • Plotly
</p>

</div>
""",
unsafe_allow_html=True
)