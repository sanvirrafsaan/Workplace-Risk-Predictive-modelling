# Option 1 — Predictive Risk Identification: Full Solution

> The complete analytical approach for the MLITSD Senior Data Scientist assignment, plus the 5-slide outline and interview talking points. This is your reference doc; the deck is the condensed version of this.

---

## 1. Case Framing (the problem in plain English)

The Ministry enforces occupational health & safety across four sectors — **Construction, Industry, Health Care, Mining** — using a case management system (FIRE). Inspectors do two kinds of work:

- **Reactive** (investigations): triggered *after* a complaint, work refusal, injury, or fatality.
- **Proactive** (inspections / consultations / campaigns): the Ministry *chooses* to go.

Inspectors are scarce. Today, proactive targeting leans on sector campaigns and inspector judgment. The Ministry wants to be **predictive**: use historical enforcement data and inspection narratives to **rank workplaces by how likely they are to have a serious safety problem**, so limited inspection capacity goes where harm is most likely.

**Why this matters (the value story):** every inspection has a cost; every prevented critical injury or fatality has an enormous human and economic cost. Better targeting means *more harm prevented per inspector-day*.

**What we must NOT do:** promise to predict *individual accidents*. We can predict *elevated risk* — a probability and severity tier — not a certainty. Saying otherwise is the fastest way to lose credibility with a technical panel.

---

## 2. Recommended Option

**Choose Option 1 (Predictive Risk Identification).**

- The role is **Senior Data Scientist**; the ad emphasizes *predictive models, statistical modelling, ML, and LLM applications*. Option 1 is the direct demonstration of those skills.
- Option 1 is **self-contained and demonstrable** in a weekend — you can ground it in the real Ontario open dataset and show actual model behavior.
- Option 2 (end-to-end platform design) is a *data-engineering / solution-architecture* showcase. It's valuable, but harder to make concrete and impressive in 5 slides without risking hand-waviness.

**Senior move:** present Option 1 as the analytical core, and close with a single "path to production" slide that gestures at the Option-2 concerns (Azure/Databricks deployment, Power BI delivery, monitoring). That shows you think end-to-end without splitting your effort.

---

## 3. Predictive Model Design

### 3.1 Unit of analysis
**The workplace** (the dictionary's core entity; NAICS, sector, region all attach to it). Roll up to the **organization/contravener** for the "high-risk organizations" framing where one entity runs multiple workplaces. Recommend: model at workplace level, aggregate scores to organization for executive reporting.

### 3.2 Target variable (the crux — get this right)

Direct prediction of fatalities/critical injuries is a **rare-event** problem (severe class imbalance, ethically fraught, reporting-biased). Instead use a **severity-weighted, learnable proxy**, with a two-tier design:

- **Primary training target (learnable):** probability that, in a forward window (e.g., next 12 months), a workplace would warrant a **serious enforcement action** — specifically **stop-work orders** and **time-unknown orders**, which *by definition* signal "immediate risk of injury to a worker." This is policy-meaningful and far less rare than fatalities.
- **Validation / north-star target:** occurrence of a **reactive serious event** (critical injury or fatality) in the forward window. We do **not** train on this directly (too rare), but we check that the risk score correlates with real harm. This keeps us honest about whether the proxy tracks actual danger.

Optionally express risk as a **rate** (per worker / per FTE using WSIB+StatsCan denominators) rather than a raw count, so large workplaces don't dominate purely by size.

> Talking point: "I deliberately predict *likelihood of a serious contravention on inspection*, not fatalities. Fatalities are too rare to model responsibly, and predicting individual accidents would be overclaiming. My proxy is severity-weighted and tied to legal definitions of immediate danger, and I validate it against actual serious-injury events."

### 3.3 The central data trap: selection / label bias
We only observe contraventions at workplaces **we chose to inspect** — labels are **missing-not-at-random**, and "found a violation" partly reflects *inspector behavior*, not just true risk. Mitigations:
- Train primarily on inspected workplaces; be explicit that scores for never-inspected sites are extrapolations.
- Prefer **proactive campaign inspections** (closer to random sampling within a sector) as a cleaner-labeled subset for validation.
- After deployment, **reserve exploratory inspection capacity** (some random/non-model-driven visits) so the model keeps learning about the whole population and doesn't just confirm its own priors.

### 3.4 Features

**Structured (from FIRE / open data):**
- *Enforcement history:* counts of orders, **stop works**, requirements, compliance commitments, BNOCs in trailing 12/24 mo; **contraventions per field visit**; escalation pattern (orders → stop works → penalties).
- *Compliance behavior:* **% orders not complied with**, % complied with, repeat outstanding orders → "willingness to comply" signal.
- *Event history:* reactive events in window — complaints, work refusals, critical/non-critical/fatal injuries, occupational illness, work stoppages; **recency** (days since last serious event).
- *Inspection cadence:* time since last inspection, number of distinct visits/inspectors, repeat-offender flag.
- *Compliance trajectory:* is the compliance rate improving or deteriorating over time?
- *Sector / NAICS baseline risk:* historical contravention/injury rate for the workplace's NAICS code (computed **out-of-fold** to avoid leakage; this is target encoding done carefully).
- *Geography:* region, district/management unit.
- *Size proxy:* number of field visits / parties / workers mentioned (or external firm-size join).
- *Temporal:* seasonality, time trends.

**Text-derived (from inspection narratives — see Section 4):**
- Hazard category, injury severity, vulnerable-worker flag (young/new/temp), supervision-failure flag, systemic-vs-one-off flag, PPE relevance, near-miss vs actual injury, root-cause category.

### 3.5 Model options (interpretable baseline → advanced)
1. **Transparent baseline:** penalized **logistic regression** (and/or a simple points-based scorecard). Gives odds ratios you can read aloud to executives. This is your "explainability floor."
2. **Performance model:** **gradient-boosted trees** (XGBoost / LightGBM) for nonlinearities and interactions.
3. **Explainability layer:** **SHAP** for global drivers + per-workplace **reason codes** ("top 3 reasons this site is high-risk"). Partial-dependence plots for executives.
4. **Calibration:** isotonic/Platt so the output reads as a true probability; bucket into **risk tiers** (Low/Med/High) by decile.
5. **(Depth, optional):** **survival / time-to-event** model for "expected time to next serious contravention" — signals sophistication if asked.

**Output:** a 0–100 risk score + tier + reason codes per workplace, refreshed monthly, fed into inspection planning.

### 3.6 Validation & evaluation
- **Temporal (out-of-time) validation**: train on past years, test on the next year. *Never* random CV here — it leaks the future and ignores how the model will actually be used.
- **Operational metric (lead with this):** **precision@k / lift in the top decile** — "of the top-N workplaces the model flags, what share have a serious finding, vs random/current targeting?" Lift is the business case.
- **Discrimination:** ROC-AUC and, because positives are rare, **PR-AUC**.
- **Calibration:** Brier score + reliability curve.
- **Baseline comparison:** vs current/random targeting, to quantify uplift in serious findings per inspection.
- **Backtest:** would the model have flagged workplaces that later had critical injuries/fatalities?
- **Monitoring in production:** performance decay, data drift, and **fairness metrics** over time.

---

## 4. LLM / NLP Use (turning inspection text into safe, useful features)

The inspection narratives (e.g., the forklift crush, the steel-tube crush involving 21- and 24-year-old workers with absent supervision, the school-yard fall) are dense with risk signal that structured fields miss: **who was hurt, how badly, whether supervision/training failed, whether the cause was systemic.**

**Approach — structured extraction with a strict schema (preferred over raw embeddings, because it's explainable):**
1. **De-identify first.** Strip worker names, addresses, and health details with PII detection *before* any modelling. Privacy is a precondition, not an afterthought.
2. **In-boundary LLM only.** Run extraction with an **in-tenant model (Azure OpenAI within the government boundary)** — no inspection data leaves to public APIs (FIPPA/PHIPPA).
3. **Schema-constrained extraction.** Prompt the LLM to return JSON, e.g.:
   ```json
   {
     "hazard_type": "struck-by / caught-in (crush)",
     "injury_severity": "critical",
     "vulnerable_worker_flag": true,
     "supervision_failure_flag": true,
     "systemic_failure_flag": true,
     "ppe_relevant": false,
     "order_sections": ["OHSA 25(2)(a)", "Reg 851 s.7"]
   }
   ```
   These become structured model features and dashboard filters.
4. **Themes (optional):** embeddings + topic modelling (e.g., BERTopic) to surface recurring hazard clusters across thousands of reports — useful for *campaign* planning, not just scoring.
5. **Human verification & guardrails:** sample-audit LLM outputs against inspector ground truth; track extraction accuracy; never let the LLM *assign enforcement* — it only structures text.

**Why not just feed raw embeddings to the model?** Embeddings boost accuracy but hurt explainability, which is fatal in a government enforcement context. Extracted, named features (e.g., "supervision failure present") are defensible to leadership and to anyone challenging an inspection decision.

---

## 5. Risks and Safeguards

| Risk | Why it matters here | Safeguard |
|---|---|---|
| **Selection / feedback bias** | Labels only exist where we inspected; targeting on the model reinforces blind spots | Reserve random/exploratory inspections; validate on proactive (near-random) visits; treat score as prioritization, not verdict |
| **Label bias** | "Found a violation" reflects inspector behavior, not only true risk | Severity-weighted target; adjust for inspection intensity; monitor inspector-level variation |
| **Fairness / disparate impact** | Could over-target small businesses, certain regions, or sectors that simply get inspected more | Audit score distribution by region/sector/firm size; exclude prohibited attributes & obvious proxies; report disparity metrics |
| **Privacy (FIPPA / PHIPPA)** | Reports contain worker names, injuries, health info | De-identify before modelling; data minimization; aggregate to workplace; access controls; keep LLM in Azure gov boundary; document lawful authority |
| **Explainability** | Enforcement decisions must be defensible | Interpretable baseline + SHAP reason codes; no black-box enforcement; publish methodology |
| **Overclaiming** | Predicting accidents erodes trust | Frame as *risk likelihood*, not certainty; communicate uncertainty/calibration |
| **Operational / data quality** | Free-text inconsistency, NAICS gaps, FIRE integration | Validation rules, fallback features, phased rollout |

**Human-in-the-loop (state this explicitly):** the model **recommends and ranks; people decide.** Inspection planners and managers see the score *and its reason codes*, can override, and their feedback flows back into retraining. The system is decision *support*, never an automated enforcement engine.

---

## 6. Five-Slide Executive Presentation Outline

> Audience: senior management. You narrate; slides stay sparse. Target ~8–10 minutes.

### Slide 1 — From Reactive to Proactive: The Opportunity
**Key message:** *We can prevent more harm with the same inspectors by predicting where serious risk is most likely.*
- Today: inspections are largely reactive or broad-campaign; inspector capacity is finite.
- Goal: rank workplaces by safety risk so proactive visits target the highest-risk sites first.
- The prize: more serious contraventions caught — and injuries prevented — per inspector-day.

### Slide 2 — The Solution at a Glance
**Key message:** *A risk-scoring engine that combines our enforcement data with inspection-report text and outputs a ranked, explainable list.*
- Inputs: structured FIRE/enforcement history + inspection narratives (via privacy-safe LLM extraction) + public sector benchmarks (WSIB/StatsCan).
- Engine: ML model → **0–100 risk score + Low/Med/High tier + top-3 reason codes** per workplace.
- Output: a monthly prioritized inspection list inside Power BI for planners. *(Simple left-to-right diagram.)*

### Slide 3 — What Predicts Risk
**Key message:** *Risk is driven by enforcement history, serious-event signals, sector baselines, compliance behavior, and hazards surfaced from text.*
- Target (state plainly): likelihood of a **serious enforcement action on inspection**, validated against actual critical injuries/fatalities — *not* a claim to predict individual accidents.
- Top drivers: prior stop-work/time-unknown orders, % orders not complied with, recent reactive events, deteriorating compliance trend, high-risk NAICS, text flags (young/new workers, supervision failure, systemic causes).
- LLM example: show the steel-tube report → extracted JSON.

### Slide 4 — Model, Validation & Expected Impact
**Key message:** *An interpretable model, validated the way it will be used, with impact measured as inspection lift.*
- Approach: transparent logistic baseline + gradient boosting; **SHAP reason codes** for explainability.
- Validation: **out-of-time** (train past → test next year); metric that matters = **lift in the top decile** vs current targeting; plus AUC/PR-AUC and calibration.
- Impact framing: "If top-decile targeting finds ~3× more serious contraventions per visit, that's the same harm prevented with a fraction of the visits." *(Show the lift chart — use real numbers if you built the prototype.)*

### Slide 5 — Responsible, Fair, and Ready to Deploy
**Key message:** *Built for a government environment: private, fair, explainable, human-in-the-loop, and deployable on our stack.*
- Privacy: FIPPA/PHIPPA, de-identification, in-boundary Azure LLM.
- Fairness: disparity audits by region/sector/size; exploration capacity to avoid feedback bias.
- Human-in-the-loop: scores **assist** planners; inspectors decide; feedback retrains.
- Roadmap: pilot in one sector/region → validate → scale on Databricks → Power BI delivery → monitor drift & fairness. *(This slide quietly answers "what about the platform?")*

---

## 7. Interview Talking Points (say these out loud)

- **Opener (problem):** "Inspectors are scarce, and most inspections happen *after* something goes wrong. I built an approach to get ahead of harm by ranking workplaces on safety risk so proactive visits go where they'll matter most."
- **On the target:** "I predict the likelihood of a *serious enforcement action on inspection* — tied to legal definitions of immediate danger — and I validate it against actual critical injuries. I deliberately don't claim to predict individual accidents; that would be overclaiming, and fatalities are too rare to model directly."
- **On bias (say it before they ask):** "The big trap is selection bias — we only have labels where we chose to inspect. If we then target purely on the model, we reinforce our own blind spots. So I'd validate on near-random campaign inspections and keep some exploratory inspection capacity."
- **On the text/LLM:** "Inspection reports hold the richest signal — supervision failures, young or new workers, systemic causes. I use an in-boundary LLM to extract a strict schema of features after de-identifying personal information, so it's both useful and FIPPA/PHIPPA-compliant."
- **On model choice:** "I pair an interpretable logistic baseline with gradient boosting, and use SHAP to give each flagged workplace its top three risk reasons — because in enforcement, an unexplainable score is unusable."
- **On evaluation:** "I validate out-of-time, the way it'll actually run, and I lead with lift in the top decile because the real question is 'do we catch more serious problems per inspection than we do today?'"
- **On responsibility:** "It's decision *support*, not automation. Planners see the score and the reasons, can override, and that feedback retrains the model. And I audit for disparate impact across region, sector, and firm size."
- **On business value:** "Better targeting means more harm prevented per inspector-day — either the same protection at lower cost, or more protection at the same cost."
- **If asked about Option 2:** *(use the 3-sentence backup from the strategy doc)*.

---

## 8. Self-check (does this answer hold up?)
- Directly answers the assignment (Option 1, predictive risk, 5 slides) — yes.
- Senior-level: leads with target definition, selection bias, privacy, and business value — yes.
- Avoids empty buzzwords: every technique is tied to a reason and an implementation detail — yes.
- Fits 5 slides — yes (outline above).
- Shows technical depth *and* government judgment — yes.
