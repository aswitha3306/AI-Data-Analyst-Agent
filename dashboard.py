import streamlit as st
import pandas as pd
import plotly.express as px
from insights import generate_insights


# ============================================
# DASHBOARD
# ============================================

def show_overview(df):

    st.header("Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing Values", int(df.isnull().sum().sum()))
    c4.metric("Duplicate Rows", int(df.duplicated().sum()))

    st.divider()

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(),
        use_container_width=True
    )

    st.divider()

    st.subheader("Column Information")

    info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(
        info,
        use_container_width=True
    )

    st.divider()

    st.subheader("Statistical Summary")

    st.dataframe(
        df.describe(include="all"),
        use_container_width=True
    )


# ============================================
# VISUALIZATIONS
# ============================================

def show_visualizations(df):

    st.header("Visualizations")

    numeric_columns = list(
        df.select_dtypes(include="number").columns
    )

    if len(numeric_columns) == 0:

        st.warning("No numeric columns found.")

        return

    column = st.selectbox(
        "Select Numeric Column",
        numeric_columns
    )

    st.subheader("Histogram")

    fig = px.histogram(
        df,
        x=column,
        nbins=30,
        title=f"Distribution of {column}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("Box Plot")

    fig = px.box(
        df,
        y=column,
        title=f"Box Plot of {column}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("Correlation Heatmap")

    corr = df[numeric_columns].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="Blues"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
# ============================================
# DATA CLEANING
# ============================================

def show_cleaning(df):

    st.header("Data Cleaning")

    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if missing.empty:

        st.success("No missing values found.")

    else:

        st.subheader("Missing Values")

        missing_df = pd.DataFrame({
            "Column": missing.index,
            "Missing Count": missing.values
        })

        st.dataframe(
            missing_df,
            use_container_width=True
        )

        fig = px.bar(
            missing_df,
            x="Column",
            y="Missing Count",
            title="Missing Values by Column"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        st.subheader("Recommended Cleaning")

        for col in missing.index:

            if pd.api.types.is_numeric_dtype(df[col]):

                st.write(
                    f"**{col}** : Fill missing values using the Median."
                )

            else:

                st.write(
                    f"**{col}** : Fill missing values using the Mode."
                )

    st.divider()

    st.subheader("Duplicate Rows")

    duplicates = int(df.duplicated().sum())

    st.metric(
        "Duplicate Rows",
        duplicates
    )

    st.divider()

    if st.button("Clean Dataset"):

        clean_df = df.copy()

        # Fill numeric columns
        for col in clean_df.select_dtypes(include="number").columns:

            clean_df[col] = clean_df[col].fillna(
                clean_df[col].median()
            )

        # Fill categorical columns
        for col in clean_df.select_dtypes(include=["object", "category"]).columns:

            if not clean_df[col].mode().empty:

                clean_df[col] = clean_df[col].fillna(
                    clean_df[col].mode()[0]
                )

        # Remove duplicates
        clean_df = clean_df.drop_duplicates()

        st.success("Dataset cleaned successfully.")

        st.subheader("Cleaned Dataset Preview")

        st.dataframe(
            clean_df.head(),
            use_container_width=True
        )

        csv = clean_df.to_csv(index=False)

        st.download_button(
            label="Download Clean Dataset",
            data=csv,
            file_name="clean_dataset.csv",
            mime="text/csv"
        )

        st.divider()

        st.subheader("Cleaning Summary")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Rows",
            clean_df.shape[0]
        )

        c2.metric(
            "Columns",
            clean_df.shape[1]
        )

        c3.metric(
            "Remaining Missing Values",
            int(clean_df.isnull().sum().sum())
        )
# ============================================
# AI INSIGHTS
# ============================================

def show_ai_insights(df):

    st.header("AI Insights")

    with st.spinner("Generating insights..."):

        insights = generate_insights(df)

    if len(insights) == 0:

        st.info("No insights generated.")

    else:

        for insight in insights:

            st.info(insight)

    st.divider()

    st.subheader("Dataset Health")

    total_missing = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    if total_missing == 0:
        st.success("No missing values found.")
    else:
        st.warning(f"{total_missing} missing values detected.")

    if duplicate_rows == 0:
        st.success("No duplicate rows found.")
    else:
        st.warning(f"{duplicate_rows} duplicate rows detected.")

    st.divider()

    st.subheader("AI Recommendation")

    recommendations = []

    if total_missing > 0:
        recommendations.append(
            "• Fill missing values before training ML models."
        )

    if duplicate_rows > 0:
        recommendations.append(
            "• Remove duplicate rows to improve data quality."
        )

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 1:
        recommendations.append(
            "• Perform correlation analysis to identify related features."
        )

    if len(df.columns) > 10:
        recommendations.append(
            "• Consider feature selection to reduce dimensionality."
        )

    if len(df) < 100:
        recommendations.append(
            "• Dataset is small. Model performance may improve with more data."
        )

    if len(recommendations) == 0:
        st.success(
            "Dataset looks clean and ready for machine learning."
        )
    else:
        for rec in recommendations:
            st.write(rec)