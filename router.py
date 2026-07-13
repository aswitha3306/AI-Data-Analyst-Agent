"""
router.py

Routes the user's question to the appropriate analysis tool.
"""

from tools import (
    get_dataset_summary,
    get_missing_values,
    get_column_info,
    get_statistics,
    get_correlation,
)

from cleaning import clean_dataset


def route_question(question, df):
    """
    Decide which tool to use based on the user's question.

    Returns:
    {
        "tool": "...",
        "result": ...
    }
    """

    question = question.lower().strip()

    # ==========================================================
    # DATASET SUMMARY
    # ==========================================================
    if any(word in question for word in [
        "summary",
        "overview",
        "dataset",
        "rows",
        "columns",
        "shape",
        "size"
    ]):

        return {
            "tool": "Dataset Summary",
            "result": get_dataset_summary(df)
        }

    # ==========================================================
    # MISSING VALUES
    # ==========================================================
    elif any(word in question for word in [
        "missing",
        "null",
        "empty",
        "nan"
    ]):

        return {
            "tool": "Missing Values",
            "result": get_missing_values(df)
        }

    # ==========================================================
    # COLUMN INFORMATION
    # ==========================================================
    elif any(word in question for word in [
        "column",
        "columns",
        "datatype",
        "data type",
        "schema",
        "feature"
    ]):

        return {
            "tool": "Column Information",
            "result": get_column_info(df)
        }

    # ==========================================================
    # STATISTICS
    # ==========================================================
    elif any(word in question for word in [
        "statistics",
        "describe",
        "mean",
        "median",
        "mode",
        "average",
        "minimum",
        "maximum",
        "min",
        "max"
    ]):

        return {
            "tool": "Statistics",
            "result": get_statistics(df)
        }

    # ==========================================================
    # CORRELATION
    # ==========================================================
    elif any(word in question for word in [
        "correlation",
        "relationship",
        "heatmap",
        "correlate"
    ]):

        return {
            "tool": "Correlation",
            "result": get_correlation(df)
        }

    # ==========================================================
    # CLEAN DATASET
    # ==========================================================
    elif any(word in question for word in [
        "clean",
        "clean dataset",
        "preprocess",
        "remove duplicates",
        "duplicates",
        "fill missing"
    ]):

        cleaned_df = clean_dataset(df)

        return {
            "tool": "Cleaning",
            "result": cleaned_df.head(10)
        }

    # ==========================================================
    # DATASET HEAD
    # ==========================================================
    elif any(word in question for word in [
        "preview",
        "head",
        "first rows",
        "show data"
    ]):

        return {
            "tool": "Dataset Preview",
            "result": df.head(10)
        }

    # ==========================================================
    # FALLBACK
    # ==========================================================
    return {
        "tool": "General",
        "result": {
            "message": "No matching tool found. Use Gemini for a general response."
        }
    }