import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.annotator import annotate_genes

st.set_page_config(page_title="Myeloma Gene Annotator", layout="wide")

st.title("🧬 Myeloma Gene Annotator")

uploaded_file = st.file_uploader("Upload a CSV file with gene symbols", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("### 📄 Preview of Uploaded File")
        st.dataframe(df.head())

        # Ensure 'Gene' column exists
        if 'Gene' not in df.columns:
            st.error("The uploaded CSV must contain a 'Gene' column.")
        else:
            gene_list = df['Gene'].dropna().unique().tolist()

            st.info(f"Found {len(gene_list)} unique gene(s) for annotation.")

            with st.spinner("🔍 Annotating genes, please wait..."):
                try:
                    annotated_df, drug_df, errors = annotate_genes(gene_list)

                    st.success("✅ Annotation completed!")

                    # Display annotations
                    st.write("### 🧬 Gene Annotations")
                    st.dataframe(annotated_df)

                    # Display drug information
                    st.write("### 💊 Drug Target Overview")
                    if drug_df is not None and not drug_df.empty:
                        st.dataframe(drug_df)
                    else:
                        st.warning("No drug target data was found for the submitted genes.")

                    # Download buttons
                    st.download_button(
                        label="📥 Download Gene Annotations",
                        data=annotated_df.to_csv(index=False),
                        file_name="gene_annotations.csv",
                        mime="text/csv",
                    )
                    if drug_df is not None and not drug_df.empty:
                        st.download_button(
                            label="📥 Download Drug Data",
                            data=drug_df.to_csv(index=False),
                            file_name="drug_targets.csv",
                            mime="text/csv",
                        )

                    # Display error summary if any
                    if errors:
                        st.write("### ❗ Error Summary")
                        for err in errors:
                            st.error(err)

                        with st.expander("🔍 Show Debug Details"):
                            st.code("\n".join(errors))

                except Exception as e:
                    st.error(f"Error during annotation: {e}")

    except Exception as e:
        st.error(f"Could not process file: {e}")
else:
    st.info("Please upload a .csv file containing a column named 'Gene'.")
