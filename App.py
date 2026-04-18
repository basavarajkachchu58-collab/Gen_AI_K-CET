import streamlit as st
import pdfplumber
import pandas as pd

st.set_page_config(page_title="KCET PDF to CSV", layout="centered")

st.title("📄 KCET PDF → CSV Converter (Improved)")
st.write("Upload KCET PDF to extract structured table data")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

def extract_tables(pdf):
    all_data = []

    for page in pdf.pages:
        tables = page.extract_tables()

        for table in tables:
            for row in table:
                if row and any(row):  # skip empty rows
                    all_data.append(row)

    return all_data


if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        table_data = extract_tables(pdf)

    if table_data:
        df = pd.DataFrame(table_data)

        # Try to set first row as header (optional)
        df.columns = df.iloc[0]
        df = df[1:]

        st.success("✅ Table extracted successfully!")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV",
            csv,
            "kcet_data.csv",
            "text/csv"
        )
    else:
        st.error("❌ No tables found in PDF")
