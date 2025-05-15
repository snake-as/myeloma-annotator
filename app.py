import streamlit as st
import pandas as pd
from annotator import annotate_genes

st.set_page_config(page_title="Myeloma Gene Annotator", layout="wide")

st.title("🧬 Myeloma Gene Annotator")
st.markdown("Upload a list of genes to receive functional and drug annotation.")

# Sidebar instructions and explanation
with st.sidebar:
    st.header("📖 How to Use")
    st.markdown("""
    1. Upload a CSV file with a column labeled `gene` (case-insensitive).
    2. The app will annotate the genes with known drug targets and biological info.
    3. Download the results as a CSV file.

    **Example CSV Format:**
    ```
    gene
    TP53
    KRAS
    NRAS
    ```

    ---
    """)

    with st.expander("🧠 How to Interpret Results"):
        st.markdown("""
        - **Gene Info:** Includes known aliases and functions from public databases.
        - **Drug Targets:** Lists drugs known to interact with or target the gene, based on DrugBank and other sources.
        - **Missing Data:** If you see `N/A`, this means no known info was found for that gene in our current database.
        - **Why Some Genes Have No Drugs:** Not all genes are druggable; many are biomarkers or play indirect roles.
        - **Data Sources:** We currently pull from DrugBank, EnrichR, and curated internal sources. More are coming!
        """)

# Upload section
uploaded_file = st.file_uploader("📁 Upload CSV with gene list", type=["csv"])

if uploaded_file is not None:
    try:
        input_df = pd.read_csv(uploaded_file)
        if 'gene' not in input_df.columns.str.lower():
            st.error("The uploaded CSV must contain a column named 'gene'.")
        else:
            # Ensure the 'gene' column exists and is standardized
            gene_col = [col for col in input_df.columns if col.lower() == 'gene'][0]
            input_df = input_df.rename(columns={gene_col: 'gene'})

            with st.spinner("🔍 Annotating genes..."):
                result_df = annotate_genes(input_df['gene'].tolist())

            st.success("✅ Annotation complete!")

            st.subheader("📋 Annotated Results")
            st.dataframe(result_df, use_container_width=True)

            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Annotated CSV",
                data=csv,
                file_name='annotated_genes.csv',
                mime='text/csv',
            )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("Please upload a CSV file with a column of gene names.")
