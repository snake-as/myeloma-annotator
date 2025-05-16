import pandas as pd
import requests
from typing import List

def annotate_genes_real_api(genes: List[str]) -> pd.DataFrame:
    """
    Query DGIdb API for drug-gene interactions and return a DataFrame
    with columns: Gene and Drug Targets.
    """
    base_url = "https://dgidb.org/api/v2/interactions.json"
    annotated_data = []

    # DGIdb allows multiple genes in one query (comma-separated)
    genes_str = ",".join(genes)

    try:
        response = requests.get(base_url, params={"genes": genes_str}, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Build a dict: gene -> list of drugs
        gene_to_drugs = {}

        for match in data.get("matchedTerms", []):
            gene_name = match.get("geneName", "")
            interactions = match.get("interactions", [])
            drugs = list({interaction.get("drugName") for interaction in interactions if interaction.get("drugName")})
            gene_to_drugs[gene_name] = drugs

        for gene in genes:
            drugs = gene_to_drugs.get(gene, [])
            annotated_data.append({
                "Gene": gene,
                "Drug Targets": ", ".join(drugs) if drugs else "None found"
            })

    except requests.RequestException:
        # If API call fails, mark all as error
        annotated_data = [{"Gene": gene, "Drug Targets": "Error fetching data"} for gene in genes]

    return pd.DataFrame(annotated_data)
