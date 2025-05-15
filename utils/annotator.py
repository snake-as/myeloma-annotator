# annotator.py

import pandas as pd
import requests
import time
from gseapy import enrichr

# Constants for external services
MYGENE_URL = "https://mygene.info/v3/query"
PHAROS_URL = "https://pharos.nih.gov/idg/api/v1/targets"
COSMIC_BASE_URL = "https://cancer.sanger.ac.uk/cosmic/api/v1"  # Hypothetical example

# Helper function for safe API calls with retries
def safe_api_call(url, params=None, retries=3, delay=1):
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(delay)
    return None

def annotate_genes(gene_list):
    annotations = []

    # Prepare gene list as comma-separated for MSigDB enrichr
    genes_str = "\n".join(gene_list)

    # MSigDB enrichment using gseapy Enrichr
    msigdb_results = None
    try:
        enr = enrichr(gene_list=gene_list, description='my_gene_list',
                      gene_sets=['MSigDB_Hallmark_2020'], outdir=None, no_plot=True)
        msigdb_results = enr.results.head(5) if enr.results is not None else None
    except Exception as e:
        msigdb_results = None

    for gene in gene_list:
        gene_data = {
            "Gene": gene,
            "Description": "",
            "Pathways (MyGene.info)": "",
            "MSigDB Hallmark Pathways": "",
            "Drugs (Pharos)": "",
            "COSMIC Mutation Info": "",
            "External Links": ""
        }

        # --- MyGene.info ---
        try:
            mg_query = safe_api_call(MYGENE_URL, params={"q": gene, "species": "human"})
            hits = mg_query.get("hits", []) if mg_query else []
            if hits:
                top_hit = hits[0]
                gene_data["Description"] = top_hit.get("summary", "")
                pathway = top_hit.get("pathway", {})
                if isinstance(pathway, dict):
                    gene_data["Pathways (MyGene.info)"] = ", ".join(pathway.keys())
        except Exception as e:
            gene_data["Description"] += f" [MyGene error: {str(e)}]"

        # --- Pharos druggability ---
        try:
            pharos_data = safe_api_call(PHAROS_URL, params={"q": gene})
            if pharos_data and "targets" in pharos_data and pharos_data["targets"]:
                dev_levels = set()
                for target in pharos_data["targets"]:
                    if "targetDevelopmentLevel" in target:
                        dev_levels.add(target["targetDevelopmentLevel"])
                gene_data["Drugs (Pharos)"] = ", ".join(dev_levels)
        except Exception as e:
            gene_data["Drugs (Pharos)"] = f"Error: {str(e)}"

        # --- COSMIC mutation info (simulated example) ---
        try:
            # This is an example URL, COSMIC API may require auth or be different
            cosmic_url = f"{COSMIC_BASE_URL}/genes/{gene}/mutations"
            cosmic_data = safe_api_call(cosmic_url)
            if cosmic_data and "mutation_count" in cosmic_data:
                gene_data["COSMIC Mutation Info"] = f"Mutations reported: {cosmic_data['mutation_count']}"
            else:
                gene_data["COSMIC Mutation Info"] = "No mutation data found"
        except Exception:
            # COSMIC API might not be accessible, fallback to no data
            gene_data["COSMIC Mutation Info"] = "Mutation data not available"

        # --- MSigDB Hallmark pathways for this gene ---
        if msigdb_results is not None:
            pathways_for_gene = msigdb_results[msigdb_results['Genes'].str.contains(gene)]
            if not pathways_for_gene.empty:
                gene_data["MSigDB Hallmark Pathways"] = ", ".join(pathways_for_gene['Term'].tolist())

        # --- External Links ---
        gene_data["External Links"] = (
            f"[GeneCards](https://www.genecards.org/cgi-bin/carddisp.pl?gene={gene}) | "
            f"[NCBI](https://www.ncbi.nlm.nih.gov/gene/?term={gene})"
        )

        annotations.append(gene_data)

    return pd.DataFrame(annotations)
