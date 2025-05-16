import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.annotator import annotate_genes

st.set_page_config(page_title="Myeloma Gene Annotator", layout="wide")

st.title("🧬 Drug Target Overview")
st.markdown("This app annotates a list of genes with enrichment data and drug target information.")

with st.sidebar:
    uploaded_file = st.file_uploader("📁 Upload a CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File loaded successfully")

        # Automatically detect gene columns (columns with name-like strings and no numbers)
        gene_columns = [col for col in df.columns if df[col].dtype == object and df[col].str.match(r'^[A-Za-z0-9-_]+$').sum() > 0]

        if not gene_columns:
            st.error("⚠️ No suitable gene columns found in the file.")
        else:
            gene_column = st.sidebar.selectbox("🧬 Select the gene column to annotate", gene_columns)

            if gene_column:
                genes = df[gene_column].dropna().unique().tolist()

                if len(genes) == 0:
                    st.warning("⚠️ The selected column contains only empty or invalid values.")
                else:
                    with st.spinner("🔎 Annotating genes, please wait..."):
                        try:
                            result_df = annotate_genes(genes)

                            if isinstance(result_df, pd.DataFrame):
                                st.success("✅ Annotation completed!")
                                st.dataframe(result_df)

                                csv = result_df.to_csv(index=False).encode('utf-8')
                                st.download_button("💾 Download Annotated CSV", csv, "annotated_genes.csv", "text/csv")

                                st.markdown("---")
                                with st.expander("🧠 Explanation / Notes"):
                                    st.markdown("""
                                    - **Missing annotations**: Genes that return no hits may not be included in some enrichment libraries.
                                    - **Empty cells**: The app automatically skips blank entries.
                                    - **Malformed genes**: Ensure gene names follow standard naming (e.g., TP53, BRCA1).
                                    - **Drug info**: Based on known drug target databases from Enrichr.
                                    """)
                            else:
                                st.error("❌ Error during annotation: Output is not a DataFrame.")

                        except Exception as e:
                            st.error(f"❌ Error during annotation: {e}")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

else:
    st.info("⬅️ Upload a gene list in CSV format using the sidebar.")
