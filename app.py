import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.annotator import annotate_genes

st.set_page_config(page_title="Myeloma Gene Annotator", layout="wide")
st.title("🧬 Drug Target Overview")

uploaded_file = st.file_uploader("Upload a CSV file with gene names", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Detect potential gene name columns
        string_columns = df.select_dtypes(include='object').columns.tolist()
        candidate_columns = [col for col in string_columns if df[col].nunique() > 1 and df[col].str.len().mean() < 20]

        if not candidate_columns:
            st.error("❌ No suitable column found that appears to contain gene names.")
        else:
            gene_col = st.selectbox("🔍 Select the column that contains gene names:", candidate_columns)
            
            # Clean and validate gene list
            genes = df[gene_col].dropna().unique().tolist()
            genes = [g.strip() for g in genes if isinstance(g, str) and g.strip() != ""]

            if genes:
                try:
                    with st.spinner("🔬 Annotating genes..."):
                        annotation_df = annotate_genes(genes)

                    st.success("✅ Annotation complete!")
                    st.dataframe(annotation_df)

                    csv = annotation_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download annotations as CSV",
                        data=csv,
                        file_name='gene_annotations.csv',
                        mime='text/csv'
                    )
                except Exception as e:
                    st.error(f"❌ Error during annotation: {e}")
            else:
                st.warning("⚠️ No valid gene names found in the selected column.")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

    with st.expander("ℹ️ What might cause errors?"):
        st.markdown("""
        - Ensure the selected column truly contains gene names (e.g. 'TP53', 'MYC').
        - Remove empty or malformed entries (e.g. blank cells).
        - Large files may take longer to process.
        - Network/API issues may interrupt annotation temporarily.
        """)
else:
    st.info("📄 Please upload a CSV file to begin.")
