import pandas as pd


def get_dataset_summary(df):
    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Column Names": list(df.columns),
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum())
    }


def get_missing_values(df):
    return df.isnull().sum()


def get_column_info(df):
    return pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values
    })


def get_statistics(df):
    return df.describe(include="all")


def get_correlation(df):
    return df.select_dtypes(include="number").corr()


def get_numeric_columns(df):
    return list(df.select_dtypes(include="number").columns)