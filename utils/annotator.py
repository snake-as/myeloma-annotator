import requests
from typing import List, Dict, Union

def clean_gene_list(genes: List[str]) -> List[str]:
    return list({g.strip().upper() for g in genes if isinstance(g, str) and g.strip()})

def fetch_drug_targets_basic(gene: str) -> List[str]:
    """Fetch drug names interacting with the gene (basic list)."""
    url = f"https://dgidb.org/api/v2/interactions.json?genes={gene}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        matched_terms = data.get("matchedTerms", [])
        drugs = []
        for term in matched_terms:
            if term.get("geneName", "").upper() == gene.upper():
                for interaction in term.get("interactions", []):
                    drug = interaction.get("drugName")
                    if drug:
                        drugs.append(drug)
        return sorted(set(drugs))
    except Exception as e:
        print(f"Error fetching drugs for gene {gene}: {e}")
        return []

def fetch_drug_targets_detailed(gene: str) -> List[Dict[str, Union[str, List[str]]]]:
    """Fetch detailed drug interaction info (drug, interaction types, sources)."""
    url = f"https://dgidb.org/api/v2/interactions.json?genes={gene}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        matched_terms = data.get("matchedTerms", [])
        interactions = []
        for term in matched_terms:
            if term.get("geneName", "").upper() == gene.upper():
                for interaction in term.get("interactions", []):
                    interactions.append({
                        "drug": interaction.get("drugName"),
                        "interaction_types": interaction.get("interactionTypes", []),
                        "sources": interaction.get("sources", []),
                    })
        return interactions
    except Exception as e:
        print(f"Error fetching detailed drugs for gene {gene}: {e}")
        return []

def annotate_genes(genes: List[str], detailed: bool = False) -> List[dict]:
    """
    Annotate genes with drug info.
    If detailed=True, return interaction type and sources per drug.
    """
    genes = clean_gene_list(genes)
    annotations = []
    for gene in genes:
        if detailed:
            interactions = fetch_drug_targets_detailed(gene)
            if interactions:
                annotations.append({"Gene": gene, "Drugs": interactions})
            else:
                annotations.append({"Gene": gene, "Drugs": []})
        else:
            drugs = fetch_drug_targets_basic(gene)
            annotations.append({"Gene": gene, "Drugs": drugs})
    return annotations
