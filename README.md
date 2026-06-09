# MLITSD Senior Data Scientist Assignment

Option 1 — Predictive Risk Identification. See `PROJECT_MASTER.md` for status and frozen decisions.

## Setup (one time)

```bash
cd "/Users/user/Desktop/Technical Project/MLITSD-DS-Project"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name=mlitsd-ds --display-name="MLITSD DS"
```

## Run notebooks

1. Activate the env: `source .venv/bin/activate`
2. Start Jupyter: `jupyter lab` (or open `.ipynb` files in Cursor/VS Code)
3. Select kernel **MLITSD DS**
4. Work through `scripts/` in order: `01_data_exploration` → `02_modeling_table` → `03_model`

## Project layout

| Path | Purpose |
|---|---|
| `PROJECT_MASTER.md` | Status, decisions, data inventory |
| `02_STEP_BY_STEP_PLAN.md` | Hour-by-hour checklist |
| `data/` | Raw downloads (do not edit) |
| `data/processed/` | Intermediate tables from notebooks |
| `scripts/` | Analysis notebooks (`01` → `03`) |
| `slides/` | Final 5-slide deck |
| `learning documents/` | `decision_log.md`, `concept_log.md` |

## Verify install

```bash
source .venv/bin/activate
python scripts/verify_env.py
```

**macOS + LightGBM:** if `import lightgbm` fails with `libomp.dylib`, run `brew install libomp`. You can also skip LightGBM and use sklearn's `HistGradientBoostingClassifier` (Phase 4 is optional).

## Packages (why each one)

| Package | Used for |
|---|---|
| pandas + openpyxl | Load `.xlsx` field visits, WSIB injury rates |
| scikit-learn | Logistic regression, metrics, lift, optional boosting |
| matplotlib + seaborn | Slide charts (lift, feature importance) |
| lightgbm + shap | Optional Phase 4 model + explainability |
| jupyter + ipykernel | Run notebooks in Cursor / Jupyter |
