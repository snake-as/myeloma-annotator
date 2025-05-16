import streamlit as st
import pandas as pd
from utils.annotator import annotate_genes, run_enrichment

st.set_page_config(page_title="Myeloma Gene Annotator", layout="wide")

st.title("🧬 Drug Target Overview")
st.markdown("Upload a gene list to get drug target annotations and pathway enrichment data.")

# Sidebar - Upload file
with st.sidebar:
    uploaded_file = st.file_uploader("📁 Upload a CSV file with gene names", type=["csv"])
    st.markdown("Your CSV should contain at least one column of gene names.")

# Main logic
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File loaded successfully!")

        # Auto-detect possible gene columns
        gene_columns = [col for col in df.columns if df[col].dtype == object and df[col].str.match(r'^[A-Za-z0-9-_]+$').sum() > 0]

        if not gene_columns:
            st.error("⚠️ No valid gene column detected. Please check your file.")
        else:
            # Let user choose gene column
            gene_column = st.sidebar.selectbox("🧬 Select gene column", gene_columns)

            if gene_column:
                genes = df[gene_column].dropna().unique().tolist()

                if not genes:
                    st.warning("⚠️ Selected column is empty or contains invalid values.")
                else:
                    with st.spinner("🔎 Annotating genes..."):
                        result_df = annotate_genes(genes)

                        if isinstance(result_df, pd.DataFrame) and not result_df.empty:
                            st.success("✅ Annotation complete!")
                            st.dataframe(result_df)

                            csv = result_df.to_csv(index=False).encode('utf-8')
                            st.download_button("💾 Download Annotated CSV", csv, "annotated_genes.csv", "text/csv")

                            st.markdown("---")
                            with st.expander("🧠 What to know"):
                                st.markdown("""
                                - **Blank entries** are skipped automatically.
                                - **Unknown genes** will return empty annotations.
                                - **Drug data** is mock/demo — you can plug in real databases later.
                                - **Enrichment analysis** support is available via `run_enrichment()`.
                                """)

                        else:
                            st.error("❌ Error during annotation: Output is not a DataFrame or is empty.")

    except Exception as e:
        st.error(f"❌ File processing error: {e}")

else:
    st.info("⬅️ Use the sidebar to upload a gene list.")
