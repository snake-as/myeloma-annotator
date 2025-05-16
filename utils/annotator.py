import requests
import pandas as pd
from typing import List, Dict

# Static fallback map (expandable)
STATIC_DRUG_MAP: Dict[str, List[str]] = {
    "TP53": ["Nutlin-3"],
    "KRAS": ["AMG-510"],
    "MYC": ["10058-F4"],
    "BRAF": ["Vemurafenib"],
    "EGFR": ["Gefitinib", "Erlotinib"],
}

def fetch_drug_targets_dgidb(gene: str) -> List[str]:
    """
    Query DGIdb API for drug interactions of a gene.
    """
    url = f"https://dgidb.org/api/v2/interactions.json?genes={gene}"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        matched_terms = data.get("matchedTerms", [])
        if not matched_terms:
            return []

        interactions = matched_terms[0].get("interactions", [])
        return sorted(set(
            i.get("drugName") for i in interactions if i.get("drugName")
        ))
    except requests.RequestException as e:
        print(f"⚠️ API error for {gene}: {e}")
        return []

def get_combined_drug_targets(gene: str) -> List[str]:
    """
    Combine API results with static map for fallback support.
    """
    api_targets = fetch_drug_targets_dgidb(gene)
    static_targets = STATIC_DRUG_MAP.get(gene.upper(), [])
    combined = set(api_targets).union(static_targets)
    return sorted(combined)

def annotate_genes(gene_list: List[str]) -> pd.DataFrame:
    """
    Annotate gene list with drug target info.
    Returns a dataframe with columns: Gene, DrugTargets, NumTargets, Source
    """
    records = []

    for gene in gene_list:
        gene = gene.strip().upper()
        drugs = get_combined_drug_targets(gene)

        record = {
            "Gene": gene,
            "DrugTargets": ", ".join(drugs) if drugs else "None",
            "NumTargets": len(drugs),
            "Status": "Annotated" if drugs else "Not Annotated",
        }
        records.append(record)

    df = pd.DataFrame(records)
    df.sort_values(by="NumTargets", ascending=False, inplace=True)
    return df
