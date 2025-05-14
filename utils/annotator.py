import requests

def annotate_gene(gene_symbol):
    result = {"Gene": gene_symbol}

    # --- Fetch gene info from MyGene.info ---
    mygene_url = f"https://mygene.info/v3/query?q={gene_symbol}&species=human"
    try:
        r = requests.get(mygene_url)
        if r.status_code == 200:
            hits = r.json().get('hits', [])
            if hits:
                hit = hits[0]
                result["Name"] = hit.get("name", "")
                result["Summary"] = hit.get("summary", "")
                result["Entrez ID"] = hit.get("entrezgene", "")
                result["Ensembl ID"] = hit.get("ensembl", {}).get("gene", "")
            else:
                result["Name"] = result["Summary"] = "Not found"
        else:
            result["Name"] = result["Summary"] = f"MyGene API error {r.status_code}"
    except Exception as e:
        result["Name"] = result["Summary"] = f"MyGene error: {str(e)}"

    # --- Fetch drug interactions from DGIdb ---
    try:
        dgidb_url = f"https://dgidb.org/api/v2/interactions.json?genes={gene_symbol}"
        r2_raw = requests.get(dgidb_url)

        # Ensure the response is valid JSON
        if r2_raw.status_code == 200 and "application/json" in r2_raw.headers.get("Content-Type", ""):
            try:
                r2 = r2_raw.json()
                drugs = r2.get('matchedTerms', [])
                if drugs and 'interactions' in drugs[0]:
                    result["Drugs"] = ', '.join([i["drugName"] for i in drugs[0]["interactions"]])
                else:
                    result["Drugs"] = "None found"
            except Exception as e:
                result["Drugs"] = f"DGIdb JSON error: {str(e)}"
        else:
            result["Drugs"] = f"DGIdb bad response ({r2_raw.status_code})"
    except Exception as e:
        result["Drugs"] = f"DGIdb error: {str(e)}"

    # --- Myeloma marker detection ---
    myeloma_markers = [
        "CCND1", "FGFR3", "MMSET", "TP53", "BCL2", "MYC", "NRAS",
        "KRAS", "IKZF1", "IKZF3", "IRF4", "XBP1"
    ]
    result["Myeloma Marker"] = "✅" if gene_symbol.upper() in myeloma_markers else ""

    return result
