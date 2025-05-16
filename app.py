import streamlit as st
import pandas as pd
from typing import List
from utils.annotator import annotate_genes_real_api

st.set_page_config(
    page_title="Drug Target Overview",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar - File Upload and Options
st.sidebar.header("Upload a CSV file")
uploaded_file = st.sidebar.file_uploader(
    "Drag and drop or browse files", type=["csv"], help="Upload your gene list CSV file"
)

st.sidebar.markdown("---")
st.sidebar.header("Instructions")
st.sidebar.markdown("""
- Upload a CSV file containing your gene list.
- Select the column in your file that contains gene symbols.
- Click the 'Annotate Genes' button to get drug target annotations from DGIdb API.
""")

# Main App
st.title("🧬 Drug Target Overview")
st.write("This app annotates a list of genes with drug target information from the DGIdb database.")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File loaded successfully")

        gene_column = st.sidebar.selectbox("Select the gene column to annotate", df.columns)

        st.subheader("📄 Uploaded Data (Preview)")
        st.dataframe(df.head())

        # Extract unique gene symbols
        genes = df[gene_column].dropna().astype(str).unique().tolist()

        if st.sidebar.button("Annotate Genes"):
            with st.spinner("Annotating genes via DGIdb API..."):
                annotated_df = annotate_genes_real_api(genes)

            # Merge original dataframe with annotations on gene column
            merged_df = pd.merge(df, annotated_df, how='left', left_on=gene_column, right_on='Gene')

            st.success("✅ Annotation completed!")

            st.subheader("📝 Annotated Data with Drug Targets")
            st.dataframe(merged_df)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

else:
    st.info("Please upload a CSV file to get started.")
