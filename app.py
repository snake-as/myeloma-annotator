import streamlit as st
import pandas as pd
from utils.annotator import annotate_genes  # Correct import

st.title("🧬 Drug Target Overview")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Uploaded Data Preview", df.head())

    gene_column = st.selectbox("Select gene column", df.columns)
    genes = df[gene_column].dropna().unique().tolist()

    with st.spinner("Annotating genes..."):
        result_df = annotate_genes(genes)
    
    st.write("### Annotated Data", result_df)
else:
    st.info("Please upload a CSV file to proceed.")
