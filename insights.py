import pandas as pd


def generate_insights(df):
    """
    Generate automatic AI dataset insights.
    """

    insights = []


    # Empty dataset check
    if df.empty:
        return [
            "⚠ Dataset is empty. Please upload a valid dataset."
        ]


    rows = df.shape[0]
    cols = df.shape[1]


    # Dataset size
    insights.append(
        f"📄 Dataset contains **{rows} rows** and **{cols} columns**."
    )


    # Missing values
    total_missing = int(df.isnull().sum().sum())


    if total_missing == 0:

        insights.append(
            "✅ No missing values found."
        )

    else:

        insights.append(
            f"⚠ Found **{total_missing} missing values**."
        )


    # Duplicate rows
    duplicates = int(df.duplicated().sum())


    if duplicates > 0:

        insights.append(
            f"⚠ Found **{duplicates} duplicate rows**. Consider removing duplicates."
        )

    else:

        insights.append(
            "✅ No duplicate rows found."
        )


    # Data types
    numeric_cols = len(
        df.select_dtypes(include="number").columns
    )

    categorical_cols = len(
        df.select_dtypes(include="object").columns
    )


    insights.append(
        f"📊 Numeric Columns: **{numeric_cols}** | "
        f"Categorical Columns: **{categorical_cols}**"
    )


    # Missing value recommendations

    for col in df.columns:

        missing_percent = (
            df[col].isnull().sum() / len(df)
        ) * 100


        if missing_percent >= 50:

            insights.append(
                f"🚨 **{col}** contains **{missing_percent:.1f}% missing values**. "
                "Consider dropping this column."
            )


        elif missing_percent > 0:


            if pd.api.types.is_numeric_dtype(df[col]):

                insights.append(
                    f"🟡 **{col}** → Recommended filling method: **Median Imputation**."
                )


            else:

                insights.append(
                    f"🟡 **{col}** → Recommended filling method: **Mode Imputation**."
                )


    # Constant columns

    constant_columns = []


    for col in df.columns:

        if df[col].nunique() == 1:

            constant_columns.append(col)


    if constant_columns:

        insights.append(
            f"⚠ Constant columns detected: **{', '.join(constant_columns)}**. "
            "Consider removing them."
        )


    # Outlier detection suggestion

    if numeric_cols > 0:

        insights.append(
            "📦 Numeric features can be checked for outliers using box plots or IQR method."
        )


    # Correlation analysis

    if numeric_cols >= 2:

        corr = df.select_dtypes(
            include="number"
        ).corr()


        high_corr = False


        for i in range(len(corr.columns)):

            for j in range(i+1, len(corr.columns)):

                if abs(corr.iloc[i,j]) > 0.8:

                    high_corr = True


        if high_corr:

            insights.append(
                "🔗 Strong correlation detected between some features. "
                "Check for multicollinearity."
            )


    # Machine Learning recommendation

    if numeric_cols >= 2:

        insights.append(
            "🤖 Dataset is suitable for Machine Learning. "
            "Try classification, regression, or clustering based on the target column."
        )

    else:

        insights.append(
            "ℹ More numerical features may be needed for ML modeling."
        )


    return insights