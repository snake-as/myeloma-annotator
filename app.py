import streamlit as st
import pandas as pd
from utils.annotator import annotate_gene

st.set_page_config(page_title="MyelomaAnnotator", layout="wide")
st.title("🧬 MyelomaAnnotator")
st.markdown("Upload a gene list to annotate them with Myeloma-specific information, drug interactions, and summaries.")

uploaded_file = st.file_uploader("📄 Upload gene list (.csv or .txt with one column)", type=["csv", "txt"])

if uploaded_file:
    gene_df = pd.read_csv(uploaded_file, header=None)
    gene_df.columns = ["Gene"]
    st.subheader("Uploaded Genes")
    st.dataframe(gene_df)

    if st.button("🔍 Annotate Genes"):
        with st.spinner("Annotating... please wait."):
            annotated = [annotate_gene(g) for g in gene_df["Gene"]]
            result_df = pd.DataFrame(annotated)
            st.success("✅ Annotation complete!")
            st.subheader("Annotated Results")
            st.dataframe(result_df)
            with st.expander("🧠 How to interpret the results"):
            st.markdown("""
            - **Gene**: The gene symbol you uploaded (e.g., `TP53`, `MYC`).
            - **Name**: Official gene name from MyGene.info.
            - **Summary**: Biological description of the gene's function.
            - **Entrez ID / Ensembl ID**: Gene database identifiers (useful for reference or further lookup).
            - **Drugs**: Drug

            csv = result_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="myeloma_annotated.csv",
                mime="text/csv"
            )
