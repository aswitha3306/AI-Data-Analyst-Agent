import pandas as pd


def clean_dataset(df):

    clean_df = df.copy()

    # Fill numeric columns
    for col in clean_df.select_dtypes(include="number").columns:
        clean_df[col] = clean_df[col].fillna(clean_df[col].median())

    # Fill categorical columns
    for col in clean_df.select_dtypes(include="object").columns:
        if not clean_df[col].mode().empty:
            clean_df[col] = clean_df[col].fillna(clean_df[col].mode()[0])

    clean_df = clean_df.drop_duplicates()

    return clean_df