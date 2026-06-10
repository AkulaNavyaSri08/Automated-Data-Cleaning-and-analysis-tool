import streamlit as st
import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------ IMPORT CORE & ANALYSIS MODULES ------------------

from core.data_loader import load_data
from core.cleaning_pipeline import clean_dataset, quality_metrics
from core.primary_key_detector import detect_primary_key

from analysis.dataset_detector import detect_dataset_type
from analysis.employee_analysis import employee_summary, top_10_paid, payroll_list
from analysis.student_analysis import marks_summary, top_students
from analysis.generic_analysis import generic_overview
from analysis.data_quality import data_quality_summary
from analysis.data_quality_score import compute_quality_score

from analysis.user_analytics import (
    descriptive_stats,
    groupby_analysis,
    top_k_analysis,
    threshold_filter,
    correlation_analysis
)

# ------------------ PAGE CONFIG ------------------

st.set_page_config(page_title="Automated Data Cleaning Tool", layout="wide")
st.title("🧠 Automated Data Cleaning & Analysis Tool")

# ------------------ FILE UPLOAD ------------------

uploaded_file = st.file_uploader("📁 Upload CSV or Excel file")

# ================== MAIN APPLICATION ==================

if uploaded_file:

    # ---------- LOAD DATA ----------
    df = load_data(uploaded_file)
    raw_df = df.copy()
    primary_key = detect_primary_key(df)

    # ---------- SESSION STATE ----------
    if "cleaned_df" not in st.session_state:
        st.session_state.cleaned_df = None

    # ---------- DATA QUALITY ----------
    quality = data_quality_summary(df)
    quality_score = compute_quality_score(
        df,
        quality["Missing Percentage (%)"],
        quality["Duplicate Rows"]
    )

    dataset_type = detect_dataset_type(df)

    # ---------- CREATE TABS ----------
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📁 Data Preview & Quality",
        "🧹 Cleaning",
        "📈 Dashboard",
        "📊 Data Visualization",
        "🧠 Analytics Toolkit"
    ])

    # ================== TAB 1: DATA PREVIEW ==================

    with tab1:
        st.subheader("📁 Dataset Information")

        st.write({
            "Rows": df.shape[0],
            "Columns": df.shape[1],
            "Primary Key": primary_key if primary_key else "Not detected",
            "Column Names": list(df.columns),
            "Numeric Columns": list(df.select_dtypes(include="number").columns),
            "Categorical Columns": list(df.select_dtypes(exclude="number").columns)
        })

        st.subheader("🔍 Dataset Preview")
        st.dataframe(df.head(20))

        st.divider()

        st.subheader("📊 Data Quality Overview")
        st.json(quality)

        st.metric("📈 Data Quality Score", f"{quality_score} / 100")

    # ================== TAB 2: CLEANING ==================

    with tab2:
        st.subheader("🧹 Dataset Cleaning")

        if st.button("Clean Dataset"):
            cleaned_df, cleaning_report = clean_dataset(df)
            st.session_state.cleaned_df = cleaned_df

            before = quality_metrics(raw_df)
            after = quality_metrics(cleaned_df)

            comparison_df = pd.DataFrame({
                "Metric": before.keys(),
                "Before Cleaning": before.values(),
                "After Cleaning": after.values()
            })

            st.subheader("🔍 Before vs After Comparison")
            st.dataframe(comparison_df)

            st.subheader("🧼 Cleaned Dataset Preview")
            st.dataframe(cleaned_df.head(20))

            buffer = io.StringIO()
            cleaned_df.to_csv(buffer, index=False)

            st.download_button(
                label="⬇️ Download Cleaned Dataset",
                data=buffer.getvalue(),
                file_name="cleaned_dataset.csv",
                mime="text/csv"
            )

            st.subheader("⚠️ Cleaning Warnings & Summary")
            st.json(cleaning_report)

            if (
                cleaning_report["Rows Removed (Null PK)"] > 0 or
                cleaning_report["Rows Removed (Duplicate PK)"] > 0
            ):
                st.warning(
                    f"Rows removed due to Primary Key issues → "
                    f"Null PK: {cleaning_report['Rows Removed (Null PK)']}, "
                    f"Duplicate PK: {cleaning_report['Rows Removed (Duplicate PK)']}"
                )

    # ================== TAB 3: DASHBOARD ==================

    with tab3:
        st.subheader("📈 Dashboard (Based on Cleaned Data)")

        if st.session_state.cleaned_df is None:
            st.warning("⚠️ Please clean the dataset to view dashboard.")
        else:
            dashboard_df = st.session_state.cleaned_df
            dataset_type = detect_dataset_type(dashboard_df)

            st.subheader(f"Detected Dataset Type: {dataset_type.upper()}")

            if dataset_type == "employee":
                st.json(employee_summary(dashboard_df))

                st.subheader("💰 Payroll List")
                st.dataframe(payroll_list(dashboard_df))

                st.subheader("🏆 Top 10 Highest Paid Employees")
                st.dataframe(top_10_paid(dashboard_df))

            elif dataset_type == "student":
                st.json(marks_summary(dashboard_df))

                st.subheader("🏆 Top 10 Students")
                st.dataframe(top_students(dashboard_df))

            else:
                st.subheader("📊 Generic Dataset Overview")
                st.json(generic_overview(dashboard_df))

    # ================== TAB 4: DATA VISUALIZATION ==================

    with tab4:
        st.header("📊 Data Visualization (Cleaned Data)")

        if st.session_state.cleaned_df is None:
            st.warning("⚠️ Please clean the dataset first to enable visualizations.")
        else:
            viz_df = st.session_state.cleaned_df

            numeric_cols = viz_df.select_dtypes(include="number").columns
            categorical_cols = viz_df.select_dtypes(exclude="number").columns

            # ---------- HISTOGRAM ----------
            if len(numeric_cols) > 0:
                st.subheader("🔢 Numeric Distribution")

                selected_num = st.selectbox("Select Numeric Column", numeric_cols)

                fig, ax = plt.subplots()
                ax.hist(viz_df[selected_num].dropna(), bins=20)
                ax.set_title(f"Distribution of {selected_num}")

                st.pyplot(fig)

                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                buf.seek(0)

                st.download_button(
                    label="⬇️ Download Histogram",
                    data=buf,
                    file_name=f"{selected_num}_histogram.png",
                    mime="image/png"
                )

            # ---------- BAR CHART ----------
            if len(categorical_cols) > 0:
                st.subheader("🔤 Categorical Frequency")

                selected_cat = st.selectbox("Select Categorical Column", categorical_cols)

                fig, ax = plt.subplots()
                viz_df[selected_cat].value_counts().head(10).plot(kind="bar", ax=ax)
                ax.set_title(f"Top Categories in {selected_cat}")

                st.pyplot(fig)

                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                buf.seek(0)

                st.download_button(
                    label="⬇️ Download Bar Chart",
                    data=buf,
                    file_name=f"{selected_cat}_barchart.png",
                    mime="image/png"
                )

            # ---------- CORRELATION HEATMAP ----------
            if len(numeric_cols) > 1:
                st.subheader("🔗 Correlation Heatmap")

                fig, ax = plt.subplots()
                sns.heatmap(viz_df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)

                st.pyplot(fig)

                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                buf.seek(0)

                st.download_button(
                    label="⬇️ Download Heatmap",
                    data=buf,
                    file_name="correlation_heatmap.png",
                    mime="image/png"
                )

    # ================== TAB 5: ANALYTICS TOOLKIT ==================

    with tab5:
        st.header("🧠 User-Driven Analytics Toolkit")

        if st.session_state.cleaned_df is None:
            st.warning("⚠️ Please clean the dataset first to enable analytics.")
        else:
            analysis_df = st.session_state.cleaned_df
            result = None

            analysis_type = st.selectbox(
                "Choose Analysis Type",
                [
                    "Descriptive Statistics",
                    "Group-By Analysis",
                    "Top-K Analysis",
                    "Threshold Filtering",
                    "Correlation Analysis"
                ]
            )

            if analysis_type == "Descriptive Statistics":
                cols = st.multiselect(
                    "Select Numeric Columns",
                    analysis_df.select_dtypes(include="number").columns
                )
                if cols:
                    result = descriptive_stats(analysis_df, cols)

            elif analysis_type == "Group-By Analysis":
                group_col = st.selectbox("Group By Column", analysis_df.columns)
                target_col = st.selectbox(
                    "Target Numeric Column",
                    analysis_df.select_dtypes(include="number").columns
                )
                agg_func = st.selectbox(
                    "Aggregation Function",
                    ["mean", "sum", "max", "min", "count"]
                )
                result = groupby_analysis(
                    analysis_df, group_col, target_col, agg_func
                )

            elif analysis_type == "Top-K Analysis":
                target_col = st.selectbox(
                    "Select Numeric Column",
                    analysis_df.select_dtypes(include="number").columns
                )
                k = st.slider("Select K", 1, 50, 10)
                result = top_k_analysis(analysis_df, target_col, k)

            elif analysis_type == "Threshold Filtering":
                col = st.selectbox(
                    "Select Numeric Column",
                    analysis_df.select_dtypes(include="number").columns
                )
                operator = st.selectbox(
                    "Operator", [">", "<", ">=", "<=", "=="]
                )
                value = st.number_input("Threshold Value")
                result = threshold_filter(analysis_df, col, operator, value)

            elif analysis_type == "Correlation Analysis":
                result = correlation_analysis(analysis_df)

            if result is not None:
                st.dataframe(result)

                csv_buf = io.StringIO()
                result.to_csv(csv_buf, index=False)

                st.download_button(
                    "⬇️ Download Analysis Result",
                    csv_buf.getvalue(),
                    "analysis_report.csv",
                    "text/csv"
                )

else:
    st.info("⬆️ Please upload a dataset to begin.")