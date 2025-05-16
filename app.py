import streamlit as st
import pandas as pd
from utils.annotator import annotate_genes

st.title("Gene Drug Annotation App")

st.markdown("""
Paste your gene list (one gene per line), then choose options to fetch drug interactions.
""")

gene_input = st.text_area("Enter genes:", height=150)
show_details = st.checkbox("Show detailed drug interaction info (types, sources)")

if st.button("Annotate Genes"):
    genes = [g.strip() for g in gene_input.strip().split("\n") if g.strip()]
    if not genes:
        st.warning("Please enter at least one gene symbol.")
    else:
        with st.spinner("Fetching drug interactions..."):
            results = annotate_genes(genes, detailed=show_details)

        # Build DataFrame for display
        if show_details:
            # Flatten detailed info into string summary per gene
            rows = []
            for res in results:
                gene = res["Gene"]
                drugs_info = res["Drugs"]
                if drugs_info:
                    for d in drugs_info:
                        interaction_types = ", ".join(d.get("interaction_types", []))
                        sources = ", ".join(d.get("sources", []))
                        rows.append({
                            "Gene": gene,
                            "Drug": d.get("drug", ""),
                            "Interaction Types": interaction_types,
                            "Sources": sources,
                        })
                else:
                    rows.append({"Gene": gene, "Drug": "None", "Interaction Types": "", "Sources": ""})

            df = pd.DataFrame(rows)
        else:
            # Simple list of drugs per gene
            df = pd.DataFrame(
                [(res["Gene"], ", ".join(res["Drugs"]) if res["Drugs"] else "None") for res in results],
                columns=["Gene", "Drugs"]
            )

        # Highlight genes with no drug annotations in yellow
        def highlight_no_drugs(row):
            if show_details:
                return ["background-color: yellow" if row["Drug"] == "None" else "" for _ in row]
            else:
                return ["background-color: yellow" if row["Drugs"] == "None" else "" for _ in row]

        st.markdown("### Annotated Genes Table")
        st.dataframe(df.style.apply(highlight_no_drugs, axis=1))
