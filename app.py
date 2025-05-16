
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.annotator import annotate_genes

st.set_page_config(page_title="Drug Target Overview", layout="wide")

st.title("🧬 Drug Target Overview")
st.markdown("This app annotates a list of genes with enrichment data and drug target information.")

# Sidebar upload
with st.sidebar:
    st.header("📂 Upload a CSV file")
    uploaded_file = st.file_uploader("Drag and drop file here", type=["csv"], help="Limit 50MB per file • CSV")

    if uploaded_file:
        st.success("✅ File loaded successfully")

    gene_column = None
    df = None

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.markdown("### 🔬 Select the gene column to annotate")
        gene_column = st.selectbox("Select the gene column to annotate", df.columns)

# Show preview of uploaded data
if uploaded_file and gene_column:
    st.subheader("📄 Uploaded Data (Preview)")
    st.dataframe(df.head(10))

    try:
        with st.spinner("🔎 Annotating genes..."):
            annotated_df = annotate_genes(df, gene_column)
            st.success("✅ Annotation completed!")

            # Merge with original dataframe
            merged_df = pd.concat([df, annotated_df], axis=1)
            st.subheader("🧪 Annotated Data (Preview)")
            st.dataframe(merged_df.head(10))

            # Show genes with actual annotations
            annotated_only = merged_df[merged_df["Drug Targets"].notna() & (merged_df["Drug Targets"] != "None found")]

            if not annotated_only.empty:
                st.subheader("🔍 Annotated Genes with Targets Found")
                st.dataframe(annotated_only)

                # Plot top genes
                st.subheader("📈 Top Genes by Number of Drug Interactions")
                annotated_only["Num Targets"] = annotated_only["Drug Targets"].apply(lambda x: len(x.split(", ")) if isinstance(x, str) and x != "None found" else 0)
                top_genes = annotated_only.sort_values("Num Targets", ascending=False).head(10)

                fig, ax = plt.subplots()
                ax.barh(top_genes[gene_column], top_genes["Num Targets"], color="#00c0ff")
                ax.invert_yaxis()
                ax.set_xlabel("Number of Drug Targets")
                ax.set_ylabel("Gene Symbol")
                st.pyplot(fig)

                # Search feature
                st.subheader("🔎 Search for a gene to view its annotations")
                search_gene = st.text_input("Enter a gene symbol:")
                if search_gene:
                    found = annotated_only[annotated_only[gene_column].str.upper() == search_gene.upper()]
                    if not found.empty:
                        st.success(f"**Drug Targets for {search_gene.upper()}**: {found['Drug Targets'].values[0]}")
                    else:
                        st.warning(f"No annotated targets found for {search_gene.upper()}")

            else:
                st.info("ℹ️ No drug targets found in the uploaded genes.")

            # Download button
            csv = merged_df.to_csv(index=False)
            st.download_button("📥 Download Annotated Data as CSV", csv, "annotated_genes.csv", "text/csv")

    except Exception as e:
        st.error(f"❌ Error during annotation: {e}")
