import streamlit as st
import pdfplumber
import pandas as pd
import re

st.set_page_config(page_title="KCET PDF to CSV", layout="centered")

st.title("📄 KCET PDF → CSV Converter")
st.write("Upload KCET allotment PDF to extract colleges, branches, CET codes.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

def extract_data_from_text(text):
    data = []

    lines = text.split("\n")

    for line in lines:
        # Example pattern (modify based on your PDF format)
        match = re.search(r'(\d{4})\s+([A-Za-z &]+)\s+([A-Za-z &]+)\s+([A-Za-z]+)', line)

        if match:
            cet_code = match.group(1)
            college = match.group(2).strip()
            branch = match.group(3).strip()
            district = match.group(4).strip()

            data.append({
                "CET Code": cet_code,
                "College": college,
                "Branch": branch,
                "District": district
            })

    return pd.DataFrame(data)

if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        full_text = ""

        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    st.success("PDF Loaded Successfully!")

    df = extract_data_from_text(full_text)

    if not df.empty:
        st.write("### Extracted Data")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="kcet_data.csv",
            mime="text/csv"
        )
    else:
        st.error("No structured data found. Try adjusting regex.")
