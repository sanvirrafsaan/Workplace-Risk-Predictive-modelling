# PowerPoint Generation Prompt — MLITSD Senior Data Scientist Interview

> **How to use this file:** Copy everything below the line `--- START PROMPT FOR CLAUDE ---` and paste it into Claude (or another AI tool). Attach or reference the chart files listed in Section 8 if the tool supports file uploads.
>
> **Your goal:** Generate a polished, interview-ready 5-slide executive PowerPoint deck + speaker notes for a **10–15 minute live presentation** (target ~10–12 min speaking time, leaving room for brief pauses and 1–2 clarifying asides).

---

## --- START PROMPT FOR CLAUDE ---

You are helping me build the **final deliverable for a Senior Data Scientist job interview** at the Ontario Ministry of Labour, Immigration, Training and Skills Development (MLITSD).

### YOUR TASK

Create a **5-slide executive PowerPoint presentation** (.pptx) with **detailed speaker notes** for each slide. The deck will be presented live to **senior government management** (mostly non-technical). I will narrate; slides must stay sparse.

**Also produce:** A separate **speaker script document** (Word or markdown) with word-for-word talking points, timed to **10–12 minutes** of speaking (max 15 minutes if I speak slowly or add one example).

---

## 1. WHAT THIS INTERVIEW IS ABOUT

### The assignment
I completed **Option 1: Predictive Risk Identification** from the MLITSD Senior Data Scientist take-home assignment.

**Business problem:** Ontario's Occupational Health and Safety (OHS) enforcement system (FIRE) captures inspection visits, orders, contraventions, and inspection report text across four sectors (Construction, Industry, Health Care, Mining). Today, inspections are largely **reactive** (after complaints, injuries, fatalities) or broad sector campaigns. **Inspectors are a scarce resource.** The Ministry wants to become **proactive** — rank workplaces by safety risk so limited inspection capacity goes where serious harm is most likely.

**My solution:** A **workplace-level risk-scoring engine** that:
- Uses structured enforcement history (Ontario open OHS field visit data, 2017–2023)
- Adds inspection-report text via **privacy-safe LLM extraction** (schema-constrained JSON, de-identified)
- Optionally enriches with **WSIB sector injury rates** as a baseline feature
- Outputs a **0–100 risk score + Low/Med/High tier + top-3 reason codes** per workplace
- Is designed to run on **Azure / Databricks / Power BI** (the Ministry's stack)

**Critical framing:** We predict **elevated risk** (likelihood of serious enforcement action on inspection), **NOT individual accidents**. Fatalities are too rare to model directly. This is decision **support**, not automated enforcement.

### The deliverable being graded
- **Required:** 5-slide executive presentation, presented live at interview
- **Optional but done:** Technical notebooks, modeling table, LLM demo, AI usage log
- **Audience:** Senior management — value story, judgment, and responsible deployment matter more than algorithm trivia

---

## 2. WHAT THE JOB POSTING WANTS (SIGNAL THESE)

The Senior Data Scientist role at MLITSD emphasizes:

| What they want | How my deck signals it |
|---|---|
| Predictive models for compliance planning | Workplace risk ranking with ~4× lift in top decile |
| Statistical modelling + ML + LLM | Logistic regression baseline, gradient boosting robustness check, LLM text extraction demo |
| Explainability for stakeholders | SHAP/permutation importance, reason codes, interpretable logistic model kept deliberately |
| Azure / Databricks / Power BI ecosystem | Solution architecture slide shows deployment on existing stack |
| FIPPA / PHIPPA privacy awareness | De-identification, in-tenant Azure LLM, no public API for sensitive data |
| Leadership & judgment | I name selection bias, overclaiming risks, and fairness BEFORE they ask |
| Briefings to senior management | Sparse slides, plain English, business metric (lift) not just AUC |
| Evidence-based decision-making | Out-of-time validation, cross-validated metrics, honest prototype caveats |

**Senior DS signals to embed throughout (not as buzzwords — as demonstrated judgment):**
1. **Correct target definition** — serious orders (Stop Work + Time Unknown), not fatalities
2. **Out-of-time validation** — train on 2017–2022, test on 2023; cross-validated
3. **Selection bias awareness** — labels only exist where we inspected; propose exploratory capacity
4. **Explainability over complexity** — boosting didn't beat logistic out-of-fold → keep simple model
5. **Privacy by design** — FIPPA/PHIPPA, de-identify before LLM
6. **Fairness** — audit by region, sector, firm size
7. **Human-in-the-loop** — model ranks; inspectors decide
8. **Honest limitations** — prototype on public open data; directional results, not production guarantee

---

## 3. DESIGN REQUIREMENTS FOR THE DECK

### Format & style
- **Exactly 5 slides** (plus optional hidden appendix slides if you include them)
- **Ministry-appropriate:** clean, professional, no clip-art, no gimmicks
- **Color palette:** blue and grey (government/professional); white backgrounds; high contrast
- **Typography:** Title 32pt+, body 24pt+; max ~6 bullet lines per slide
- **One key visual per slide** — charts or simple diagrams, not walls of text
- **Sparse slides, rich speaker notes** — I am the narration; slides are anchors

### Charts to embed (I will provide these image files)
| Slide | File | Description |
|---|---|---|
| Slide 3 (left panel) | `data/processed/feature_importance.png` | Top feature drivers (permutation importance) |
| Slide 4 | `data/processed/lift_chart.png` | Decile lift chart — top decile ~4× baseline |

If you cannot embed images, leave a clearly labeled placeholder box with the filename and dimensions.

### Slide 3 right panel — LLM before/after (recreate as a visual)
**Before (de-identified excerpt from Sample Report 2 — steel tube crush):**
> A worker was critically injured when steel tubes fell during unloading. The worker was 21 years old, employed for two weeks, and working without direct supervision. The employer had no documented training program for the task.

**After (LLM extraction JSON):**
```json
{
  "hazard_type": "caught-in / crush",
  "injury_severity": "critical",
  "vulnerable_worker_flag": true,
  "supervision_failure_flag": true,
  "systemic_failure_flag": true,
  "order_sections": ["OHSA 25(2)(a)", "Reg 851 s.7"]
}
```

Show this as a clean before → after panel. Caption: *"Text adds what structured fields miss."*

---

## 4. REAL NUMBERS TO USE (DO NOT INVENT OR ROUND AGGRESSIVELY)

These come from my actual analysis notebooks. Use them consistently across slides and speaker notes.

| Metric | Value |
|---|---|
| Evaluation cohort | **12,234 workplaces** (with history 2017–2022 AND a 2023 visit) |
| Baseline serious-order rate | **8.0%** |
| Top-decile serious-order rate | **32.5%** (in-sample) / **~32%** (cross-validated) |
| **Primary result: Lift @ top 10%** | **~4.0×** (in-sample 4.08×, cross-validated 4.00×) |
| Lift @ top 10% (LightGBM, CV) | **3.73×** — does NOT beat logistic |
| PR-AUC / ROC-AUC (logistic, CV) | **0.31 / 0.80** |
| Top structured drivers | Industry sector, prior orders/investigations, recency, compliance rate |
| Train/test design | Features through **2022-12-31** → target = serious order in **2023** |
| Serious order types (2023) | Stop Use/Stop Work Order, Time Unknown Order |
| Data source | Ontario OHS field visit open data (2017–2023), ~120k rows/year |

**Key talking-point numbers (I must know these cold):**
- **4× lift** in the top decile
- **32% vs 8%** serious-order rate (top decile vs baseline)

**Honesty guardrail (must appear in Slide 4 speaker notes):**
> "This is a prototype on public open data. Metrics are directional, not a production guarantee."

---

## 5. THE 5 SLIDES — EXACT CONTENT

### SLIDE 1 — From Reactive to Proactive
**Title:** Targeting Inspections Where Risk Is Highest

**Key message (subtitle or callout):** *We can prevent more harm with the same inspectors by predicting where serious risk concentrates.*

**Bullets (keep to 4):**
- Today, inspections are largely **reactive** (after complaint, injury, or fatality) or broad sector campaigns
- Inspector capacity is finite; most workplaces are never visited in a given year
- **Opportunity:** rank workplaces by safety risk so proactive visits target highest-risk sites first
- **The prize:** more serious problems caught — and injuries prevented — per inspector-day

**Visual:** Simple left-to-right arrow or funnel:
`All workplaces → Risk-ranked shortlist → Proactive inspections where risk is highest`

**Speaker notes (~1 min):**
Open with: "Thanks for the time. I chose **Option 1 — Predictive Risk Identification**. I'll show how the Ministry can use its own enforcement data, plus inspection-report text, to target inspections more proactively — and I'll be upfront about the limits."

Then: "Today, most inspections happen **reactively** — after a complaint, an injury, or a fatality — or through broad sector campaigns. But inspectors are a scarce resource, and in any given year most workplaces are never visited. The opportunity is to get **ahead** of harm: rank workplaces by safety risk, so our proactive visits go where risk is highest. The goal isn't more inspections — it's **more harm prevented per inspector-day**."

---

### SLIDE 2 — The Solution at a Glance
**Title:** A Risk-Scoring Engine for Inspection Planning

**Key message:** *Combine enforcement history with inspection-report text to produce a ranked, explainable shortlist.*

**Bullets (keep to 4):**
- **Inputs:** enforcement & visit history (FIRE / Ontario open data) + inspection-report text (privacy-safe LLM extraction) + sector benchmarks (WSIB)
- **Engine:** ML model → **0–100 risk score + Low/Med/High tier + top-3 reason codes** per workplace
- **Output:** monthly prioritized inspection list in **Power BI** for planners
- **Stack:** designed for **Azure / Databricks / Power BI**

**Visual:** Pipeline diagram (left to right):
```
Structured data + Text → Feature engineering → Risk model → Score + reason codes → Power BI
```

**Speaker notes (~1.5 min):**
"Here's the solution in one picture. We combine three inputs: our **enforcement and visit history**, the **text in inspection reports**, and **sector injury benchmarks** from WSIB.

That feeds a model that outputs, for each workplace, a **risk score from 0 to 100**, a tier — low, medium, high — and the **top three reasons** it scored that way.

Planners would see this as a prioritized list in **Power BI**. And it's all designed to run on the stack we already use — **Azure, Databricks, Power BI**."

---

### SLIDE 3 — What Predicts Risk
**Title:** What the Data Says Drives Risk

**Key message:** *Risk is driven by enforcement history, recency, sector, and hazards from text — and we can explain every score.*

**Bullets (keep to 3–4):**
- **Target (be precise):** likelihood of a **serious enforcement action** (stop-work / time-unknown order) on inspection — validated against serious injuries. *We do not predict individual accidents.*
- **Top structured drivers:** prior orders & investigations, stop-work history, time since last visit, compliance rate, **industry sector** (construction & mining highest)
- **Text adds what structured fields miss:** LLM converts narratives into features — supervision failure, young/new worker, systemic cause

**Visual (two-panel layout):**
- **Left:** `feature_importance.png` (bar chart of top drivers)
- **Right:** LLM before/after example (steel-tube report → JSON, see Section 3)

**Speaker notes (~2–2.5 min):**
"Let me be precise about **what we predict**, because it matters. We predict the likelihood a workplace receives a **serious enforcement action** — a stop-work or time-unknown order, which by definition signal immediate danger — on its next inspection. We validate that against actual serious injuries. **We deliberately do not claim to predict individual accidents** — that would be overclaiming, and fatalities are too rare to model responsibly.

The strongest drivers are intuitive: **prior orders and investigations, stop-work history, how recently we've been there, compliance behaviour, and industry sector** — construction and mining rank highest.

The interesting part is the **text**. Structured fields don't capture *why* something happened. So we use an LLM to turn a narrative into structured features. On the right is a real example — a crush incident: the model extracts that it was a **critical injury**, involved **young, new workers**, a **supervision failure**, and a **systemic cause** — not a worker-compliance issue. Those become features and dashboard filters."

---

### SLIDE 4 — Does It Work? Validation & Impact
**Title:** Validated the Way It Would Be Used

**Key message:** *Targeting the top-scored workplaces finds ~4× more serious problems per inspection than the baseline.*

**Bullets (keep to 4):**
- **Honest validation:** trained on history (2017–2022), tested on next year (2023); **cross-validated**, not in-sample
- **Result: ~4× lift in the top decile** — top-scored workplaces: **32% serious-order rate vs 8% baseline**
- **Robustness:** gradient boosting matched the simple model out-of-fold → signal is real; we keep the **explainable** model with no accuracy penalty
- **Business translation:** same harm prevented with fewer visits — or more harm prevented with the same budget

**Visual:** `lift_chart.png` — decile bar chart showing monotonic lift, top decile ~4×

**Speaker notes (~2–2.5 min):**
"Does it work? I validated it the way it would actually run: I trained on history through 2022 and tested on 2023 — predicting the future from the past, and cross-validated so the numbers aren't inflated.

The headline: about a **4× lift in the top decile**. The workplaces the model flags as highest-risk had a **32% serious-order rate, versus an 8% baseline**. In plain terms — if we inspected that top group, we'd find serious problems about **four times more often** than untargeted visits.

I also stress-tested it with gradient boosting. Out-of-fold, the complex model **didn't beat** the simple one — which tells me two things: the signal is **real**, and we can keep the **fully explainable** model with no accuracy penalty. That's the right trade for enforcement.

One honesty note: this is a prototype on **public open data**, so these are **directional** results, not a production guarantee."

---

### SLIDE 5 — Responsible, Fair & Ready to Deploy
**Title:** Built for a Government Environment

**Key message:** *Private, fair, explainable, human-in-the-loop, and deployable on our stack.*

**Bullets (keep to 5, short):**
- **Privacy (FIPPA/PHIPPA):** de-identify reports before processing; LLM **in-tenant on Azure** — no data to public APIs
- **Fairness:** audit scores for disparate impact by region, sector, and firm size
- **Avoid feedback bias:** reserve **random/exploratory** inspections so the model keeps learning the whole population
- **Human-in-the-loop:** the model **ranks; inspectors decide.** Reason codes make every score reviewable
- **Roadmap:** pilot one sector/region → validate → scale on Databricks → monitor drift & fairness

**Visual:** Four icons or a simple timeline:
`Pilot → Validate → Scale (Databricks) → Monitor`

**Speaker notes (~2 min):**
"Finally — and for a government context this is the most important slide — how we do this responsibly.

**Privacy:** reports contain personal and health information, so we de-identify before processing and keep the LLM **in-tenant on Azure** — no data leaves to public APIs. That's FIPPA and PHIPPA aligned.

**Fairness:** we audit the scores for disparate impact across region, sector, and firm size, so we're not just over-targeting small businesses or one region.

**Bias:** because we only have labels where we chose to inspect, targeting purely on the model could reinforce our blind spots — so I'd reserve some **random, exploratory** inspections to keep learning.

**And critically — this is decision support, not automation.** The model **ranks; inspectors decide.** Every score comes with its reasons, so it's reviewable and defensible.

The path forward is a **pilot** in one sector, validate, then scale on Databricks with monitoring for drift and fairness."

**Closing line (~15 sec, after Slide 5):**
"So: a credible, explainable way to put inspectors where risk is highest — about **4× more efficient** at finding serious problems — built privately and fairly on our existing tools. Happy to go deeper on any part."

---

## 6. OPTIONAL APPENDIX SLIDES (HIDDEN — FOR Q&A ONLY)

If you include appendix slides, mark them clearly as backup and do NOT count toward the 5-slide limit.

| Slide | Title | Content |
|---|---|---|
| A1 | Target Definition & Selection Bias | Serious order strings; evaluation cohort definition; why labels are MNAR |
| A2 | Model Metrics Table | Logistic vs LightGBM: lift, PR-AUC, ROC-AUC (in-sample vs CV) |
| A3 | Feature Dictionary | Top 10 features with definitions |
| A4 | LLM Extraction Prompt | Schema + FIPPA-safe prompt example |

---

## 7. Q&A PREP (INCLUDE IN SPEAKER SCRIPT APPENDIX)

| Likely question | Crisp answer |
|---|---|
| "How is this better than what inspectors already know?" | "It complements them. It scans every workplace consistently across 800k+ records no person can hold in their head — then gives the inspector the reasons, so their judgment stays in charge." |
| "What's your biggest limitation?" | "Selection bias — we only have outcomes where we inspected. I mitigate it with exploratory inspections and by validating on near-random campaign visits. Scores for never-visited sites are extrapolations." |
| "Why not the fancier model / deep learning?" | "I tested gradient boosting; it didn't beat logistic out-of-fold. In enforcement, an unexplainable score is unusable, so I won't add complexity that doesn't pay for itself." |
| "Is 4× real?" | "It's a cross-validated estimate on public data — directional, not a guarantee. A production pilot with internal FIRE data would confirm it." |
| "Privacy / can you even use the text?" | "Yes, with controls: de-identification, data minimization, in-tenant LLM, access controls, documented lawful authority. The LLM only structures text — it never assigns enforcement." |
| "What would you need to deploy?" | "Access to FIRE data, Azure OpenAI in-boundary, Databricks job for monthly scoring, Power BI surface for planners, plus governance sign-off on fairness and privacy." |
| "How often does it run?" | "Monthly scoring is plenty for inspection planning, with model retraining and fairness/drift checks on a regular cadence." |

---

## 8. WHAT NOT TO DO

- Do NOT claim we predict individual accidents or fatalities
- Do NOT use jargon without plain-English translation (AUC, SHAP, etc. only if briefly explained)
- Do NOT overcrowd slides — if in doubt, cut text and put it in speaker notes
- Do NOT use stock photos, cartoons, or flashy animations
- Do NOT invent metrics — use only the numbers in Section 4
- Do NOT make the deck look like a consulting pitch deck — this is a government ministry interview
- Do NOT skip Slide 5 (privacy/fairness/human-in-the-loop) — it is what lands with senior gov leaders

---

## 9. OUTPUT FORMAT REQUESTED

Please deliver:

1. **PowerPoint file (.pptx)** with:
   - 5 main slides as specified above
   - Speaker notes on every slide (full script from Section 5)
   - Placeholders or embedded charts where noted
   - Optional appendix slides (clearly separated)

2. **Speaker script (markdown or Word)** with:
   - Full word-for-word script for 10–12 minutes
   - Timing markers per slide (e.g., "Slide 1: ~1 min")
   - Opening and closing lines
   - Q&A appendix from Section 7
   - Rehearsal checklist:
     - [ ] Can state target definition without notes
     - [ ] Can explain selection bias in one sentence
     - [ ] Know two numbers cold: 4× lift, 32% vs 8%
     - [ ] Privacy + human-in-the-loop close practiced

3. **Design notes** (brief): font choices, color hex codes used, any assumptions about chart placement

---

## 10. CONTEXT ABOUT ME (TONE CALIBRATION)

- I am interviewing for a **Senior** Data Scientist role — the deck should signal **judgment and ownership**, not "I ran a notebook."
- I made every major analytical decision myself (target variable, train/test split, model choice, metric selection, bias mitigation framing). AI tools assisted with code and drafting under my direction.
- If asked about AI usage, I will cite `AI_USAGE.md` transparently.
- The interview panel will likely include both technical and non-technical senior leaders. Slide 4 is for the technical folks; Slides 1, 2, and 5 are for everyone.

---

## --- END PROMPT FOR CLAUDE ---

---

## Quick reference: files to attach when generating

When pasting the prompt into Claude, also attach or upload these if possible:

| File | Purpose |
|---|---|
| `data/processed/lift_chart.png` | Slide 4 chart |
| `data/processed/feature_importance.png` | Slide 3 left panel |
| `data/processed/llm_extraction_example.json` | Slide 3 LLM example (if you want exact JSON) |

## After Claude generates the deck

1. Review Slide 3 target sentence — must say "serious enforcement action," NOT "predict accidents"
2. Verify Slide 4 numbers: **4× lift**, **32% vs 8%**
3. Rehearse from speaker notes twice, timed (target 10–12 min)
4. Export PDF backup
5. Come back to Cursor for code walkthrough prep if interviewers probe the notebooks
