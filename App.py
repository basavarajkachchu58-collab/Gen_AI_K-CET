import streamlit as st
import pdfplumber
import pandas as pd

st.set_page_config(page_title="KCET PDF to CSV", layout="centered")

st.title("📄 KCET PDF → CSV Converter (Fixed)")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

def extract_tables(pdf):
    all_rows = []

    for page in pdf.pages:
        tables = page.extract_tables()

        for table in tables:
            for row in table:
                if row and any(row):
                    all_rows.append(row)

    return all_rows


def clean_dataframe(df):
    # Remove completely empty columns
    df = df.dropna(axis=1, how='all')

    # Fill NaN with empty string
    df = df.fillna("")

    # Make column names unique
    new_cols = []
    for i, col in enumerate(df.columns):
        if col in new_cols:
            new_cols.append(f"{col}_{i}")
        else:
            new_cols.append(col if col != "" else f"Column_{i}")

    df.columns = new_cols
    return df


if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        data = extract_tables(pdf)

    if data:
        df = pd.DataFrame(data)

        # ❗ DO NOT blindly assign first row as header
        # Instead clean first
        df = clean_dataframe(df)

        st.success("✅ Data extracted successfully!")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV",
            csv,
            "kcet_data.csv",
            "text/csv"
        )
    else:
        st.error("❌ No table found in PDF")
