import pandas as pd
from gseapy import enrichr
from typing import List

# Enrichr databases to use
enrichr_libraries = [
    "KEGG_2021_Human",
    "WikiPathway_2021_Human",
    "BioPlanet_2019",
    "ChEA_2016",
    "Drug_Perturbations_from_GEO_2014"
]

def clean_gene_list(genes: List[str]) -> List[str]:
    """Remove empty, NaN, duplicates and strip whitespace."""
    cleaned = list({g.strip() for g in genes if isinstance(g, str) and g.strip()})
    return cleaned

def fetch_drug_targets(gene: str) -> List[str]:
    """Mock: fetch drug targets for gene (replace with real DB query)."""
    drug_map = {
        "TP53": ["Nutlin-3"],
        "KRAS": ["AMG-510"],
        "MYC": ["10058-F4"]
    }
    return drug_map.get(gene.upper(), [])

def annotate_genes(genes: List[str]) -> pd.DataFrame:
    """Annotate genes with drug targets and return a DataFrame."""
    genes = clean_gene_list(genes)
    results = []
    for gene in genes:
        try:
            drugs = fetch_drug_targets(gene)
            results.append({
                "gene": gene,
                "drugs": ", ".join(drugs) if drugs else ""
            })
        except Exception as e:
            results.append({
                "gene": gene,
                "drugs": "",
                "error": str(e)
            })

    df = pd.DataFrame(results)
    return df

def run_enrichment(genes: List[str]) -> pd.DataFrame:
    """Run enrichment analysis using Enrichr."""
    genes = clean_gene_list(genes)
    if not genes:
        return pd.DataFrame()
    enr = enrichr(gene_list=genes, description='gene_enrichment', gene_sets=enrichr_libraries)
    if enr.results is not None:
        return enr.results
    return pd.DataFrame()
