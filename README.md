# MLITSD Senior Data Scientist Assignment

Option 1 — Predictive Risk Identification. A workplace-level risk model built on Ontario's public OHS field visit data (2017–2023), achieving ~4x lift in serious enforcement findings in the top-scored decile.

See `TECHNICAL_DOCUMENTATION.md` for methodology, decisions, and limitations. AI tool usage is documented in `AI_USAGE.md` as required by the brief.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name=mlitsd-ds --display-name="MLITSD DS"
```

Verify the environment:

```bash
python scripts/verify_env.py
```

**macOS + LightGBM:** if `import lightgbm` fails with `libomp.dylib`, run `brew install libomp`. LightGBM is only needed for the optional robustness check in notebook 04.

## Running the analysis

Activate the env, open the notebooks in Jupyter or Cursor/VS Code with the **MLITSD DS** kernel, and run in order:

1. `scripts/01_data_exploration.ipynb` — EDA, schema checks across years, base rates
2. `scripts/02_modeling_table.ipynb` — workplace-level features + target
3. `scripts/03_model.ipynb` — logistic regression, lift chart, coefficients
4. `scripts/04_boosting_shap.ipynb` — LightGBM robustness check (optional)

## Project layout

| Path | Purpose |
|---|---|
| `TECHNICAL_DOCUMENTATION.md` | Methodology, modeling decisions, limitations |
| `AI_USAGE.md` | AI tool usage log (required by brief) |
| `data/` | Raw downloads (do not edit) |
| `data/processed/` | Modeling table and chart outputs from notebooks |
| `scripts/` | Analysis notebooks (01 → 04) |
| `files/` | Executive slide deck (5 slides) and speaker script |
| `Reference documents/` | Assignment brief, job posting, data dictionary |

## Packages

| Package | Used for |
|---|---|
| pandas + openpyxl | Load `.xlsx` field visits and WSIB injury rates |
| scikit-learn | Logistic regression, metrics, lift |
| matplotlib + seaborn | Lift chart, feature importance chart |
| lightgbm | Optional boosting robustness check |
| jupyter + ipykernel | Notebooks |
