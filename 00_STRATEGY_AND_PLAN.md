# Strategy & Weekend Plan — MLITSD Senior Data Scientist Assignment

> Your one-page-ish "what do I actually do?" guide. Read this first. Everything else flows from here.

---

## 0. The 30-second version

You are being asked to show that you can turn the Ministry's **enforcement data + messy inspection text** into a **predictive risk score** that tells inspectors **which workplaces to visit next**. The deliverable that gets scored is a **5-slide executive deck** you present live. Everything else (code, docs) is optional supporting evidence that makes you look senior.

**Decision: Do Option 1 (Predictive Risk Identification).** It directly demonstrates the ML + LLM + statistical-modelling skills the job ad screens for, and it is the thing you can make concrete in a weekend. Keep one paragraph of Option 2 ("how I'd productionize this") as a backup talking point — do **not** build both.

---

## 1. What is actually being asked (decode the brief)

The brief gives you two options. Read between the lines:

- **Option 1 = "show me you can model."** Analytical capability, statistics, ML, LLM. This is a *data science* showcase.
- **Option 2 = "show me you can architect a data platform."** Pipelines, integration, data modelling, Azure/Databricks. This is a *data engineering / solution design* showcase.

The **job title is "Senior Data Scientist"** and the ad repeatedly says *predictive models, statistical modelling, ML, LLM applications*. Option 1 is the bullseye. Option 2 is a legitimate alternate skillset they listed because they're hiring multiple people — it is not "better," it's "different." Pick the one that shows YOUR strength and that you can execute well in the time you have. For almost anyone interviewing for a *data scientist* seat, that's Option 1.

### The real business problem (say it in plain English in the interview)
> "Today the Ministry mostly inspects **reactively** — after a complaint, injury, or fatality — or via broad sector campaigns. Inspectors are a scarce resource. The Ministry wants to get **ahead** of harm by predicting *which workplaces are most likely to have a serious safety problem* and sending inspectors there **first**. My job is to build a credible, fair, explainable way to rank workplaces by risk."

---

## 2. The single most important insight (this is what separates senior from junior)

You were **not given an actual dataset** — only a data dictionary, 3 sample reports, and the brief. That is deliberate. Two things follow:

1. **You don't need to build a perfect model on real data.** You need to demonstrate *the thinking*: correct target definition, sensible features, the right model choices, and — critically — awareness of the **traps** (selection bias, rare events, privacy, fairness). Senior candidates win on judgment, not on accuracy numbers.

2. **The data dictionary hands you a public dataset on a plate.** Under "Open Data" it literally points to:
   > *Occupational health and safety field visits, workplaces visited, and orders issued — Ontario Data Catalogue.*

   That dataset is real, free, and downloadable (2012–2024, one CSV per year). It contains: **field visit date, visit type, case type (inspection vs investigation), case status, workplace ID/name/location, NAICS code, contravener name/role, and orders issued.** That is enough to build a *real, demonstrable* prototype risk model — which is what turns a good deck into a great one.

   Links:
   - Field visits / orders dataset: https://data.ontario.ca/dataset/occupational-health-and-safety-field-visits-workplaces-visited-and-orders-issued
   - OHS inspections report (summary): https://data.ontario.ca/dataset/occupational-health-and-safety-inspections-report

**So: yes, there ARE files you can download.** That was the hint in the documents.

---

## 3. Data you have vs. data you can get

| Source | What's in it | How you use it |
|---|---|---|
| **Data dictionary (provided)** | Definitions of cases, events, contraventions, orders, stop works, compliance statuses, NAICS, sector, region | Your feature dictionary. Mine it for risk signals (esp. **stop work**, **time-unknown orders**, **% not complied with**, **reactive events**). |
| **Sample inspection reports (provided)** | 3 free-text narratives (forklift crush, steel-tube crush w/ young workers, school fall) | Your **NLP/LLM demo material**. Show how text → structured features (hazard type, severity, young/new worker flag, supervision failure, systemic vs one-off). |
| **Ontario OHS open dataset (download)** | Field visits, orders, NAICS, region, dates, 2012–2024 | Build a **real prototype**: workplace-level risk features + a model that ranks workplaces by future order likelihood. Optional but high-impact. |
| **WSIB open data + StatsCan (optional)** | Injury/lost-time-claim rates by NAICS sector; business counts; FTEs | **Sector base-rate** features and to express risk as a *rate* (per worker) not a raw count. Adds maturity. WSIB: https://www.wsib.ca/en/open-data-catalogue |

> Rule from your brief: only bring in *public* data, and **cite every source and every AI tool you use**. Keep an `AI_USAGE.md` log as you go (the brief requires it).

---

## 4. The weekend plan (≈10–12 hours)

You have a week but ~10–12 focused hours on the weekend, then behavioral prep. Here's a realistic split. **The deck is the priority. Code is a bonus that you should time-box hard.**

### Saturday (≈6 hrs)
- **(45 min) Absorb the case.** Re-read `01_SOLUTION_Option1_Predictive_Risk.md` (the full solution doc). Make sure you can explain the *target variable* and *selection bias* in your own words. These are the two things interviewers probe.
- **(45 min) Download + eyeball the data.** Grab 2–3 recent years of the Ontario OHS CSV. Open in Excel/pandas. Confirm columns. You don't need to model yet — just be able to say "I worked with the actual data."
- **(2.5 hrs) Build the minimal prototype (optional but recommended).** Aggregate to workplace level, engineer ~10 features, train a logistic regression + gradient boosting to predict "workplace receives an order on its next visit," report AUC and **lift in the top decile**, make a SHAP/feature-importance chart. One notebook. Stop when it runs end-to-end — do NOT polish.
- **(1 hr) LLM/NLP demo.** Take the 3 sample reports, write one prompt that extracts a strict JSON schema (hazard_type, severity, vulnerable_worker_flag, supervision_failure_flag, systemic_flag, order_sections). Save the input + output. This is your "text → features" proof.
- **(45 min) Pull 1–2 charts/numbers you'll actually put on slides.** Top risk factors, the lift chart, the JSON extraction example.

### Sunday (≈5–6 hrs)
- **(3 hrs) Build the 5 slides.** Use the outline in the solution doc verbatim as your skeleton. One message per slide. Drop in your charts. Keep text sparse — you are the narration.
- **(1 hr) Write speaker notes / talking points** (the solution doc gives you these). Practice the "problem in plain English" opener and the "here's how I avoid bias and protect privacy" closer.
- **(1 hr) Dry run out loud, twice.** Time it (~8–10 min for 5 slides). Cut anything you stumble on.
- **(30 min) Finalize `AI_USAGE.md`** and a short technical appendix linking the notebook (optional).

### If you're short on time, cut in this order:
1. Cut the StatsCan/WSIB enrichment (just *mention* it as future work).
2. Cut the gradient boosting model (logistic regression alone is fine and *more* explainable).
3. Cut the live code entirely — a strong conceptual deck still scores well. **Never cut: clear target definition, the bias/privacy slide, and rehearsal.**

---

## 5. What "senior" looks like in the room (how you get hired)

Interviewers for a senior gov DS role are listening for **judgment**, not jargon. Score points by:

- **Defining the target carefully and admitting its flaws.** "I predict likelihood of a *serious enforcement action on inspection* as a proxy for danger, because true fatalities are too rare to model directly and predicting individual accidents would be overclaiming."
- **Naming the selection-bias trap unprompted.** "We only have labels for workplaces we *chose* to inspect, and if we then send inspectors based on the model, we reinforce our own blind spots — so I'd reserve some random/exploratory inspection capacity."
- **Leading with privacy.** FIPPA/PHIPPA, the reports contain worker health info, de-identify before modelling, keep LLM processing inside the Azure government boundary (no data to public APIs).
- **Translating to business value.** "If the top-decile model finds 3× more serious contraventions per inspection than current targeting, that's the same harm prevented with a third of the visits — or 3× the harm prevented with the same budget."
- **Showing the production path** (this quietly answers Option 2): pilot → validate against held-out year → deploy scoring in Databricks → surface scores + reason codes in Power BI for inspection planners → monitor drift and fairness.

### Backup Option-2 answer (memorize 3 sentences in case asked)
> "If the priority were the platform rather than the model, I'd design an end-to-end pipeline on Azure/Databricks: ingest FIRE + open + WSIB data into a curated workplace table, add a governed text-processing layer that de-identifies and structures inspection narratives with an in-tenant LLM, serve a monthly risk score to Power BI for planners, and wrap it in monitoring for data drift, model performance, and fairness. The model I'm presenting today is the analytical core that platform would operationalize."

---

## 6. Deliverables checklist

- [ ] **5-slide deck** (the graded artifact) — follow the outline in the solution doc.
- [ ] Speaker notes / talking points memorized.
- [ ] (Optional) One clean notebook: data → features → model → lift chart → SHAP.
- [ ] (Optional) LLM extraction example (input report + JSON output).
- [ ] `AI_USAGE.md` documenting every AI tool used (required by the brief).
- [ ] Sources cited (Ontario Data Catalogue, WSIB, StatsCan if used).
- [ ] Behavioral prep (separate; budget time after the deck is done).

---

## 7. Files in this repo

- `00_STRATEGY_AND_PLAN.md` — this file.
- `01_SOLUTION_Option1_Predictive_Risk.md` — the full analytical solution + 5-slide outline + talking points.
- `MLITSD_Senior_Data_Scientist_Job_Posting.md`, `senior_data_scientist_assignment_brief.md`, `ohs_bosta_data_dictionary.md`, `sample_inspection_reports.md` — provided source materials.
- (Create as you work) `notebooks/`, `AI_USAGE.md`, `slides/`.
