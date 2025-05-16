import pandas as pd
from gseapy import enrichr
from typing import List, Dict

# List of enrichment libraries
enrichr_libraries = [
    "KEGG_2021_Human",
    "WikiPathway_2021_Human",
    "BioPlanet_2019",
    "ChEA_2016",
    "Drug_Perturbations_from_GEO_2014"
]

def clean_gene_list(genes: List[str]) -> List[str]:
    return list({g.strip() for g in genes if isinstance(g, str) and g.strip()})

def fetch_drug_targets(gene: str) -> List[str]:
    drug_map = {
        "TP53": ["Nutlin-3"],
        "KRAS": ["AMG-510"],
        "MYC": ["10058-F4"]
    }
    return drug_map.get(gene.upper(), [])

def annotate_genes(genes: List[str]) -> pd.DataFrame:
    genes = clean_gene_list(genes)
    records = []

    for gene in genes:
        try:
            record = {
                "Gene": gene,
                "Drugs": ", ".join(fetch_drug_targets(gene))
            }
            records.append(record)
        except Exception as e:
            records.append({"Gene": gene, "Drugs": "", "Error": str(e)})

    return pd.DataFrame(records)

def run_enrichment(genes: List[str]) -> pd.DataFrame:
    genes = clean_gene_list(genes)
    if not genes:
        return pd.DataFrame()

    enr = enrichr(gene_list=genes, description='gene_enrichment', gene_sets=enrichr_libraries)
    return enr.results if enr.results is not None else pd.DataFrame()
