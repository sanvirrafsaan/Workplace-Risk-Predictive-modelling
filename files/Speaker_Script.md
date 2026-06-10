# Speaker Script — Predictive Risk Identification
### MLITSD Senior Data Scientist Interview · 5-slide live presentation

**Target speaking time: 10–12 minutes** (max ~15 if you slow down or add one example).
Deck: `MLITSD_Risk_Identification.pptx` · Charts embedded on Slides 3 & 4 · Appendix A1–A4 are backup for Q&A only.

> **One-line framing to hold in your head:** *We predict elevated risk of serious enforcement action — not individual accidents. This is decision support, not automation.*

---

## OPENING — before advancing to Slide 1 (~10 sec)

"Thanks for the time. I chose **Option 1 — Predictive Risk Identification**. I'll show how the Ministry can use its own enforcement data, plus inspection-report text, to target inspections more proactively — and I'll be upfront about the limits."

---

## SLIDE 1 — Targeting Inspections Where Risk Is Highest (~1 min)

"Today, most inspections happen **reactively** — after a complaint, an injury, or a fatality — or through broad sector campaigns. But inspectors are a scarce resource, and in any given year most workplaces are never visited.

The opportunity is to get **ahead** of harm: rank workplaces by safety risk, so our proactive visits go where risk is highest. The goal isn't more inspections — it's **more harm prevented per inspector-day**."

*[Advance to Slide 2]*

---

## SLIDE 2 — A Risk-Scoring Engine for Inspection Planning (~1.5 min)

"Here's the solution in one picture. We combine three inputs: our **enforcement and visit history**, the **text in inspection reports**, and **sector injury benchmarks** from WSIB.

That feeds a model that outputs, for each workplace, a **risk score from 0 to 100**, a tier — low, medium, high — and the **top three reasons** it scored that way.

Planners would see this as a prioritized list in **Power BI**. And it's all designed to run on the stack we already use — **Azure, Databricks, Power BI**."

*[Advance to Slide 3]*

---

## SLIDE 3 — What the Data Says Drives Risk (~2 to 2.5 min)

"Let me be precise about **what we predict**, because it matters. We predict the likelihood a workplace receives a **serious enforcement action** — a stop-work or time-unknown order, which by definition signal immediate danger — on its next inspection. We validate that against actual serious injuries. **We deliberately do not claim to predict individual accidents** — that would be overclaiming, and fatalities are too rare to model responsibly.

*[gesture to left chart]* The strongest drivers are intuitive: **prior orders and investigations, stop-work history, how recently we've been there, compliance behaviour, and industry sector** — construction and mining rank highest.

*[gesture to right panel]* The interesting part is the **text**. Structured fields don't capture *why* something happened. So we use an LLM to turn a narrative into structured features. On the right is a real example — a crush incident: the model extracts that it was a **critical injury**, involved **young, new workers**, a **supervision failure**, and a **systemic cause** — not a worker-compliance issue. Those become features and dashboard filters."

*[Advance to Slide 4]*

---

## SLIDE 4 — Validated the Way It Would Be Used (~2 to 2.5 min)

"Does it work? I validated it the way it would actually run: I trained on history through 2022 and tested on 2023 — predicting the future from the past — and **cross-validated** so the numbers aren't inflated.

The headline: about a **4× lift in the top decile**. The workplaces the model flags as highest-risk had a **32% serious-order rate, versus an 8% baseline**. In plain terms — if we inspected that top group, we'd find serious problems about **four times more often** than untargeted visits.

I also stress-tested it with gradient boosting. Out-of-fold, the complex model **didn't beat** the simple one — which tells me two things: the signal is **real**, and we can keep the **fully explainable** model with no accuracy penalty. That's the right trade for enforcement.

One honesty note: this is a prototype on **public open data**, so these are **directional** results, not a production guarantee."

*[Advance to Slide 5]*

---

## SLIDE 5 — Built for a Government Environment (~2 min)

"Finally — and for a government context this is the most important slide — how we do this responsibly.

**Privacy:** reports contain personal and health information, so we de-identify before processing and keep the LLM **in-tenant on Azure** — no data leaves to public APIs. That's FIPPA and PHIPPA aligned.

**Fairness:** we audit the scores for disparate impact across region, sector, and firm size, so we're not just over-targeting small businesses or one region.

**Bias:** because we only have labels where we chose to inspect, targeting purely on the model could reinforce our blind spots — so I'd reserve some **random, exploratory** inspections to keep learning.

**And critically — this is decision support, not automation.** The model **ranks; inspectors decide.** Every score comes with its reasons, so it's reviewable and defensible.

The path forward is a **pilot** in one sector, validate, then scale on Databricks with monitoring for drift and fairness."

---

## CLOSING — after Slide 5 (~15 sec)

"So: a credible, explainable way to put inspectors where risk is highest — about **4× more efficient** at finding serious problems — built privately and fairly on our existing tools. Happy to go deeper on any part."

---

## TIMING SUMMARY

| Section | Target |
|---|---|
| Opening | ~10 sec |
| Slide 1 | ~1 min |
| Slide 2 | ~1.5 min |
| Slide 3 | ~2–2.5 min |
| Slide 4 | ~2–2.5 min |
| Slide 5 | ~2 min |
| Closing | ~15 sec |
| **Total** | **~10–12 min** |

---

## Q&A APPENDIX (have Appendix slides A1–A4 ready to pull up)

| Likely question | Crisp answer |
|---|---|
| **How is this better than what inspectors already know?** | "It complements them. It scans every workplace consistently across hundreds of thousands of records no person can hold in their head — then gives the inspector the reasons, so their judgment stays in charge." |
| **What's your biggest limitation?** | "Selection bias — we only have outcomes where we inspected. I mitigate it with exploratory inspections and by validating on near-random campaign visits. Scores for never-visited sites are extrapolations." *(pull up A1)* |
| **Why not the fancier model / deep learning?** | "I tested gradient boosting; it didn't beat logistic out-of-fold. In enforcement, an unexplainable score is unusable, so I won't add complexity that doesn't pay for itself." *(pull up A2)* |
| **Is 4× real?** | "It's a cross-validated estimate on public data — directional, not a guarantee. A production pilot with internal FIRE data would confirm it." |
| **Privacy / can you even use the text?** | "Yes, with controls: de-identification, data minimization, in-tenant LLM, access controls, documented lawful authority. The LLM only structures text — it never assigns enforcement." *(pull up A4)* |
| **What would you need to deploy?** | "Access to FIRE data, Azure OpenAI in-boundary, a Databricks job for monthly scoring, a Power BI surface for planners, plus governance sign-off on fairness and privacy." |
| **How often does it run?** | "Monthly scoring is plenty for inspection planning, with model retraining and fairness/drift checks on a regular cadence." |

---

## REHEARSAL CHECKLIST

- [ ] Can state the **target definition** without notes (*serious enforcement action — stop-work / time-unknown order — NOT individual accidents*)
- [ ] Can explain **selection bias in one sentence** (*we only have labels where we chose to inspect*)
- [ ] Know **two numbers cold**: **4× lift** · **32% vs 8%**
- [ ] **Privacy + human-in-the-loop close** practiced (FIPPA/PHIPPA · in-tenant Azure · model ranks, inspectors decide)
- [ ] Rehearsed **twice, timed** — landing in the 10–12 min window
- [ ] **PDF backup** exported in case of AV issues
- [ ] Appendix slides A1–A4 located and quick to jump to during Q&A

---

## NUMBERS REFERENCE (do not misquote)

- Evaluation cohort: **12,234 workplaces** (history 2017–2022 + a 2023 visit)
- Baseline serious-order rate: **8.0%**
- Top-decile serious-order rate: **~32%**
- **Lift @ top 10%: ~4.0×** (in-sample 4.08×, cross-validated 4.00×)
- LightGBM lift @ top 10% (CV): **3.73×** — does *not* beat logistic
- Logistic PR-AUC / ROC-AUC (CV): **0.31 / 0.80**
- Train/test: features through **2022-12-31** → target = serious order in **2023**
- Serious order types (2023): **Stop Use / Stop Work Order, Time Unknown Order**
