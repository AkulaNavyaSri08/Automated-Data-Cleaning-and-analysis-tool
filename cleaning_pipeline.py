import pandas as pd
from analysis.data_quality import data_quality_summary
from analysis.data_quality_score import compute_quality_score

from core.primary_key_detector import detect_primary_key
from core.datatype_handler import fix_datatypes


def clean_dataset(df):
    df = df.copy()

    pk_col = detect_primary_key(df)

    dropped_null_pk = 0
    dropped_duplicate_pk = 0

    if pk_col:
        dropped_null_pk = df[pk_col].isna().sum()
        df = df[df[pk_col].notna()]

        df["_completeness_"] = df.notna().sum(axis=1)
        before_dup = len(df)

        df = (
            df.sort_values("_completeness_", ascending=False)
              .drop_duplicates(subset=pk_col)
              .drop(columns="_completeness_")
        )

        dropped_duplicate_pk = before_dup - len(df)

    df = fix_datatypes(df)

    for col in df.columns:
        if col == pk_col:
            continue

        if df[col].dtype.kind in "biufc":
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
        else:
            mode_series = df[col].mode()
            if not mode_series.empty:
                df[col] = df[col].fillna(mode_series.iloc[0])

    cleaning_report = {
        "Primary Key Used": pk_col if pk_col else "Not detected",
        "Rows Removed (Null PK)": dropped_null_pk,
        "Rows Removed (Duplicate PK)": dropped_duplicate_pk,
        "Final Row Count": len(df)
    }

    return df, cleaning_report


def quality_metrics(df):
    quality = data_quality_summary(df)

    score = compute_quality_score(
        df,
        quality["Missing Percentage (%)"],
        quality["Duplicate Rows"]
    )

    quality["Quality Score"] = score

    return quality