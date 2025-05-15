import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.annotator import annotate_genes
import time

st.set_page_config(page_title="Myeloma Gene Annotator", layout="wide")

# Sidebar information
with st.sidebar:
    st.title("🧬 Gene Annotator")
    st.markdown("""
    Welcome to the **Myeloma Gene Annotator**!

    -> Upload a `.csv` file with a column of gene names.  
    -> View annotations from:
    - Enrichr (pathways, ontologies)
    - DrugBank, DGIdb (targets)
    - GeneCards, COSMIC (info)

    ⚠️ Empty or invalid gene entries will be skipped.

    ---
    [GitHub Repo](https://github.com/yourrepo)  
    Made with ❤️ using Streamlit
    """)

st.title("📊 Drug Target Overview")
uploaded_file = st.file_uploader("Upload a CSV file with gene names", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        gene_column = df.columns[0]
        genes = df[gene_column].dropna().astype(str).str.strip().unique().tolist()

        if not genes:
            st.warning("No valid genes found in the uploaded file.")
        else:
            with st.spinner("🔍 Annotating genes, please wait..."):
                results = annotate_genes(genes)
                time.sleep(1)  # simulate delay

            st.success("✅ Annotation complete!")
            st.subheader("Annotation Summary")

            for section, table in results.items():
                if table.empty:
                    st.warning(f"No data found for section: {section}")
                    continue
                st.markdown(f"### {section}")
                st.dataframe(table)

    except Exception as e:
        st.error("❌ Error processing file: " + str(e))
        st.markdown("""
        ### What went wrong?
        This error might occur due to:
        - Missing or incorrectly named gene column
        - Empty rows or invalid characters
        - Incompatible file format

        ✅ Please ensure:
        - The file is a valid `.csv`
        - The first column contains gene names
        - No completely empty rows or duplicate header rows exist
        """)

else:
    st.info(" Please upload a gene list to begin.")
