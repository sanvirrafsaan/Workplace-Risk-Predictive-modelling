# Notebooks

Run in order:

| Notebook | Phase | Purpose |
|---|---|---|
| `01_eda.ipynb` | 1 | Load data, schema check, order type counts |
| `02_modeling_table.ipynb` | 2 | Workplace-level features + target |
| `03_model.ipynb` | 3–4 | Logistic regression, lift, optional SHAP |

**Conventions:**
- Raw data lives in `data/` — never modify those files
- Save intermediate tables to `data/processed/` if needed (create folder when you get there)
- Every notebook starts with a markdown cell: goal, inputs, outputs, decisions referenced (D00X)
