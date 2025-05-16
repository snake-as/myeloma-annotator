import streamlit as st
import pandas as pd
from utils.annotator import annotate_genes  # Make sure this path is correct

st.set_page_config(
    page_title="Drug Target Overview",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar - upload file and select gene column
st.sidebar.header("Upload a CSV file")
uploaded_file = st.sidebar.file_uploader(
    "Drag and drop or browse files", type=["csv"], help="Upload your gene list CSV file"
)

st.sidebar.markdown("---")
st.sidebar.header("Instructions")
st.sidebar.markdown("""
- Upload a CSV file containing your gene list.
- Select the column in your file that contains gene symbols.
- The app will annotate your genes with drug target information.
""")

# Main content
st.title("🧬 Drug Target Overview")
st.write("This app annotates a list of genes with enrichment data and drug target information.")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File loaded successfully")

        # Select gene column to annotate
        gene_column = st.sidebar.selectbox("Select the gene column to annotate", df.columns)

        # Show preview of uploaded data
        st.subheader("📄 Uploaded Data (Preview)")
        st.dataframe(df.head())

        # Extract gene list from selected column
        genes = df[gene_column].dropna().astype(str).unique().tolist()

        # Run annotation
        with st.spinner("Annotating genes..."):
            annotated_df = annotate_genes(genes)

        st.success("✅ Annotation completed!")

        # Show annotated results
        st.subheader("📝 Annotated Genes")
        st.dataframe(annotated_df)

    except Exception as e:
        st.error(f"❌ Error during annotation: {str(e)}")

else:
    st.info("Please upload a CSV file to get started.")
