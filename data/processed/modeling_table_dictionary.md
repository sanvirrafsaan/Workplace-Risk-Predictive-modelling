# Modeling Table Data Dictionary

**File:** `data/processed/modeling_table.csv`  
**Built in:** `scripts/02_modeling_table.ipynb`  
**Grain:** 1 row = 1 workplace (`workplace_id`)  
**Rows:** 12,234  
**Decisions:** D004 (target), D005 (out-of-time split), D007 (schema), D008 (cohort), D009 (serious orders)

---

## Table design

| Item | Definition |
|------|------------|
| Feature window | 2017-01-01 through 2022-12-31 (snapshot date: 2022-12-31) |
| Target window | Calendar year 2023 |
| Cohort | Workplaces with ≥1 visit in 2017–2022 **and** ≥1 visit in 2023 |
| Source data | Ontario OHS field visit open data, 2017–2023 xlsx files |

---

## Columns

| Column | Type | Definition | How computed | Notes |
|--------|------|------------|--------------|-------|
| `workplace_id` | int | Ministry FIRE workplace identifier | From `WORKPLACE ID` | Primary key; unique per row |
| `n_visits_5y` | int | Distinct field visits in feature window | Count of unique (`WORKPLACE ID`, `FIELD VISIT DATE`) pairs, 2017–2022 | Not row count — one visit can have multiple order rows |
| `n_investigations_5y` | int | Reactive visits in feature window | Distinct visits where `CASE TYPE` = `Investigation` | Investigations follow complaints, injuries, etc. |
| `days_since_last_visit` | int | Days from last historical visit to snapshot | `(2022-12-31 − max(FIELD VISIT DATE)).days` per workplace | 0 = visited on snapshot date; uses history only |
| `primary_naics` | float | Primary industry code | Mode of `PRIMARY NAICS` across feature-window rows | NAICS 2017; 4 rows null (no NAICS in history) |
| `n_orders_5y` | int | Enforcement orders issued | Count of rows with non-null `ORDER TYPE` | Row-level count; visit-only rows excluded |
| `n_stop_work_5y` | int | Stop work orders in history | Count where `ORDER TYPE` = `Stop Use/Stop Work Order` | 2017–2023 files use this label (D009) |
| `n_time_unknown_5y` | int | Time unknown orders in history | Count where `ORDER TYPE` = `Time Unknown Order` | Signals immediate compliance deadline uncertainty |
| `pct_complied_5y` | float | Share of orders marked complied | `Complied With` count ÷ orders with non-null `ORDER STATUS` | Null if workplace had no orders with status (~30% of rows) |
| `investigation_ratio` | float | Fraction of visits that were investigations | `n_investigations_5y` ÷ `n_visits_5y` | Range 0–1; reactive-visit intensity |
| `target_serious_2023` | int (0/1) | **Target** — serious order in 2023 | 1 if workplace received ≥1 `Stop Use/Stop Work Order` or `Time Unknown Order` in 2023; else 0 | **Not a feature** — do not use in training features |

---

## Target (`target_serious_2023`)

| Value | Meaning | Count | Share |
|-------|---------|-------|-------|
| 0 | No serious order in 2023 | 11,260 | 92.0% |
| 1 | ≥1 serious order in 2023 | 974 | 8.0% |

Serious order types (2023 labels, D009):
- `Stop Use/Stop Work Order`
- `Time Unknown Order`

---

## Summary statistics (features)

| Column | Min | Median | Mean | Max |
|--------|-----|--------|------|-----|
| `n_visits_5y` | 1 | 3 | 5.5 | 241 |
| `n_investigations_5y` | 0 | 1 | 3.6 | 228 |
| `days_since_last_visit` | 0 | 304 | 523 | 2,186 |
| `n_orders_5y` | 0 | 3 | 6.8 | 771 |
| `n_stop_work_5y` | 0 | 0 | 0.4 | 95 |
| `n_time_unknown_5y` | 0 | 0 | 0.6 | 171 |
| `pct_complied_5y` | 0.0 | 1.0 | 0.96 | 1.0 |
| `investigation_ratio` | 0.0 | 0.54 | 0.51 | 1.0 |

---

## Caveats for modeling

1. **Selection bias (D006):** Labels exist only where the Ministry inspected. Cohort restricts to revisited workplaces; scores for never-inspected sites are extrapolations.
2. **`pct_complied_5y` nulls:** Impute or add a missing indicator before logistic regression.
3. **`primary_naics`:** Treat as categorical (or sector rollup) in Phase 3 — not a continuous numeric.
4. **No random train/test split:** Features ≤2022, target in 2023 — split is already out-of-time (D005).
