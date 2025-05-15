import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from annotator import annotate_genes

st.set_page_config(page_title="Myeloma Gene Annotator", layout="wide")

st.title("🧬 Myeloma Gene Annotator")
st.markdown("Upload a list of genes to receive functional and drug annotation.")

# Sidebar instructions and explanation
with st.sidebar:
    st.header("📖 How to Use")
    st.markdown("""
    1. Upload a CSV, TXT, or Excel file with a column labeled `gene` (case-insensitive).
    2. The app will annotate the genes with known drug targets and biological info.
    3. Download the results or explore the visualizations.

    **Example Format:**
    ```
    gene
    TP53
    KRAS
    NRAS
    ```
    """)

    with st.expander("🧠 How to Interpret Results"):
        st.markdown("""
        - **Gene Info:** Includes known aliases and functions from public databases.
        - **Drug Targets:** Lists drugs known to interact with or target the gene.
        - **Missing Data:** `N/A` means no known info was found for that gene.
        - **Why Some Genes Have No Drugs:** Not all genes are druggable.
        - **Data Sources:** DrugBank, EnrichR, and more.
        """)

# Upload section
uploaded_file = st.file_uploader("📁 Upload gene list", type=["csv", "txt", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".xlsx"):
            input_df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".txt"):
            input_df = pd.read_csv(uploaded_file, sep="\t")
        else:
            input_df = pd.read_csv(uploaded_file)

        gene_col = [col for col in input_df.columns if col.lower() == 'gene']
        if not gene_col:
            st.error("The uploaded file must contain a column named 'gene'.")
        else:
            input_df = input_df.rename(columns={gene_col[0]: 'gene'})

            with st.spinner("🔍 Annotating genes..."):
                result_df = annotate_genes(input_df['gene'].tolist())

            st.success("✅ Annotation complete!")

            st.subheader("📋 Annotated Results")
            st.dataframe(result_df, use_container_width=True)

            # Visualization section
            st.subheader("📊 Drug Target Overview")
            drug_counts = result_df['drugs'].value_counts().drop(labels=['N/A'], errors='ignore')
            if not drug_counts.empty:
                fig, ax = plt.subplots()
                sns.barplot(y=drug_counts.index, x=drug_counts.values, ax=ax)
                ax.set_xlabel("# of Genes")
                ax.set_ylabel("Drug")
                st.pyplot(fig)
            else:
                st.info("No drug annotations available for visualization.")

            # Download option
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
    st.info("Please upload a file with a column of gene names.")
