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
    st.markdown("---")
    st.markdown("""
    ### How to use:
    1. Upload a CSV file.
    2. Choose the gene column.
    3. View annotations and download results.
    """)

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File loaded successfully")
        st.subheader("📄 Uploaded Data (Preview)")
        st.dataframe(df.head(10))

        gene_columns = [col for col in df.columns if df[col].dtype == object and df[col].str.match(r'^[A-Za-z0-9-_]+$').sum() > 0]

        if not gene_columns:
            st.error("⚠️ No suitable gene columns found.")
        else:
            gene_column = st.sidebar.selectbox("🧬 Select gene column", gene_columns)

            if gene_column:
                genes = df[gene_column].dropna().unique().tolist()

                if len(genes) == 0:
                    st.warning("⚠️ Column is empty.")
                else:
                    with st.spinner("🔎 Annotating genes..."):
                        try:
                            annotation_df = annotate_genes(genes)

                            if isinstance(annotation_df, pd.DataFrame):
                                st.success("✅ Annotation completed!")
                                merged_df = df.merge(annotation_df, left_on=gene_column, right_on="Gene", how="left")
                                
                                st.subheader("🔬 Annotated Data Preview")
                                st.dataframe(merged_df.head(10))

                                st.download_button("💾 Download Annotated CSV", merged_df.to_csv(index=False).encode('utf-8'), "annotated_genes.csv", "text/csv")

                                st.markdown("---")
                                st.subheader("📊 Annotation Summary")
                                annotated = annotation_df[annotation_df['NumTargets'] > 0]
                                not_annotated = annotation_df[annotation_df['NumTargets'] == 0]

                                fig, ax = plt.subplots()
                                sns.barplot(
                                    x=["Annotated", "Not Annotated"],
                                    y=[len(annotated), len(not_annotated)],
                                    palette="muted",
                                    ax=ax
                                )
                                ax.set_ylabel("Number of Genes")
                                st.pyplot(fig)

                                st.markdown("### 🔎 Example Drug Targets")
                                st.dataframe(annotated.head(10))

                                with st.expander("ℹ️ Notes"):
                                    st.markdown("""
                                    - **Real-time data** from DGIdb.
                                    - Only genes found in the drug interaction database will be annotated.
                                    - Drugs shown may be experimental or FDA-approved.
                                    """)

                            else:
                                st.error("❌ Annotation did not return a DataFrame.")

                        except Exception as e:
                            st.error(f"❌ Error during annotation: {e}")

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

else:
    st.info("⬅️ Upload a CSV to begin.")
