# 🧬 Myeloma Annotator

**Myeloma Annotator** is a free, interactive web tool that allows researchers and clinicians to quickly annotate gene lists (e.g., from RNA-seq or panel sequencing) with relevant biological insights for **Multiple Myeloma (MM)**.

Built with 🐍 Python and ⚡️ Streamlit, the app helps make gene lists actionable by highlighting:
- Associated biological functions
- Drug interactions (clinical or preclinical)
- Involvement in MM or other cancers
- Summary descriptions from public databases

🔗 **Live App**: [https://myeloma-annotator-jtmdcz6wt7ijrsvbeomrhd.streamlit.app/ ] 
📘 **Demo CSV file**: [`example_genes.csv`](./example_genes.csv)

---

## 🧪 What Problem Does This Solve?

Many researchers generate gene lists from transcriptomic or genomic analysis but lack a fast way to:
- Understand what each gene *does*
- See if any *targetable drugs* exist
- Prioritize genes for experimental validation in **MM**

This tool offers a **concise, interpreted report** for each gene — saving you hours of manual searching.

---

## ⚙️ How It Works

1. Upload a `.csv` file with your list of gene names (1 gene per row)
2. The tool will:
   - Retrieve a plain-language gene summary
   - Search drug–gene interactions (via DrugBank & other sources)
   - Highlight MM-specific relevance (e.g., differential expression, biomarkers)
3. View and explore:
   - 🧠 Annotated summaries
   - 💊 Drug relevance section
   - 📤 Exportable annotated results as `.csv`

---

## 🖥️ Run Locally (Dev Mode)

Make sure you have Python 3.9+ installed.

```bash
git clone https://github.com/snake-as/myeloma-annotator.git
cd myeloma-annotator
pip install -r requirements.txt
streamlit run app.py


📂 Project Structure
bash
Copy
Edit
.
├── app.py                # Main Streamlit interface
├── annotator.py          # Core annotation logic
├── requirements.txt      # Python dependencies
├── example_genes.csv     # Demo gene list
└── README.md             # This file

🙌 Credits
Developed by Feidias — Biomedical Data Science & AI in Medicine
