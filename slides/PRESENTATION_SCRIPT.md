# Presentation Script (Speaker Notes)

> Word-for-word-ish script to rehearse. Aim ~8–9 min, leaving room for Q&A.
> Don't read it — internalize the **bolded** anchors per slide. Pause after each key number.

---

## Opening (before Slide 1, ~15 sec)
"Thanks for the time. I chose **Option 1 — Predictive Risk Identification**. I'll show how the Ministry can use its own enforcement data, plus inspection-report text, to target inspections more proactively — and I'll be upfront about the limits."

---

## SLIDE 1 — From Reactive to Proactive (~1 min)
"Today, most inspections happen **reactively** — after a complaint, an injury, or a fatality — or through broad sector campaigns. But inspectors are a scarce resource, and in any given year most workplaces are never visited.

The opportunity is to get **ahead** of harm: rank workplaces by safety risk, so our proactive visits go where risk is highest. The goal isn't more inspections — it's **more harm prevented per inspector-day**."

---

## SLIDE 2 — The Solution at a Glance (~1.5 min)
"Here's the solution in one picture. We combine three inputs: our **enforcement and visit history**, the **text in inspection reports**, and **sector injury benchmarks** from WSIB.

That feeds a model that outputs, for each workplace, a **risk score from 0 to 100**, a tier — low, medium, high — and the **top three reasons** it scored that way.

Planners would see this as a prioritized list in **Power BI**. And it's all designed to run on the stack we already use — **Azure, Databricks, Power BI**."

---

## SLIDE 3 — What Predicts Risk (~2 min)
"Let me be precise about **what we predict**, because it matters. We predict the likelihood a workplace receives a **serious enforcement action** — a stop-work or time-unknown order, which by definition signal immediate danger — on its next inspection. We validate that against actual serious injuries. **We deliberately do not claim to predict individual accidents** — that would be overclaiming, and fatalities are too rare to model responsibly.

The strongest drivers are intuitive: **prior orders and investigations, stop-work history, how recently we've been there, compliance behaviour, and industry sector** — construction and mining rank highest.

The interesting part is the **text**. Structured fields don't capture *why* something happened. So we use an LLM to turn a narrative into structured features. On the right is a real example — a crush incident: the model extracts that it was a **critical injury**, involved **young, new workers**, a **supervision failure**, and a **systemic cause** — not a worker-compliance issue. Those become features and dashboard filters."

---

## SLIDE 4 — Validation & Impact (~2 min)
"Does it work? I validated it the way it would actually run: I trained on history through 2022 and tested on 2023 — predicting the future from the past, and cross-validated so the numbers aren't inflated.

The headline: about a **4× lift in the top decile**. The workplaces the model flags as highest-risk had a **32% serious-order rate, versus an 8% baseline**. In plain terms — if we inspected that top group, we'd find serious problems about **four times more often** than untargeted visits.

I also stress-tested it with gradient boosting. Out-of-fold, the complex model **didn't beat** the simple one — which tells me two things: the signal is **real**, and we can keep the **fully explainable** model with no accuracy penalty. That's the right trade for enforcement.

One honesty note: this is a prototype on **public open data**, so these are **directional** results, not a production guarantee."

---

## SLIDE 5 — Responsible & Ready (~2 min)
"Finally — and for a government context this is the most important slide — how we do this responsibly.

**Privacy:** reports contain personal and health information, so we de-identify before processing and keep the LLM **in-tenant on Azure** — no data leaves to public APIs. That's FIPPA and PHIPPA aligned.

**Fairness:** we audit the scores for disparate impact across region, sector, and firm size, so we're not just over-targeting small businesses or one region.

**Bias:** because we only have labels where we chose to inspect, targeting purely on the model could reinforce our blind spots — so I'd reserve some **random, exploratory** inspections to keep learning.

**And critically — this is decision support, not automation.** The model **ranks; inspectors decide.** Every score comes with its reasons, so it's reviewable and defensible.

The path forward is a **pilot** in one sector, validate, then scale on Databricks with monitoring for drift and fairness."

---

## Close (~15 sec)
"So: a credible, explainable way to put inspectors where risk is highest — about **4× more efficient** at finding serious problems — built privately and fairly on our existing tools. Happy to go deeper on any part."

---

## Q&A — likely questions + crisp answers

**"How is this better than what inspectors already know?"**
"It complements them. It scans every workplace consistently and surfaces patterns across 800k+ records no person can hold in their head — then gives the inspector the reasons, so their judgment stays in charge."

**"What's your biggest limitation?"**
"Selection bias — we only have outcomes where we inspected. I mitigate it with exploratory inspections and by validating on near-random campaign visits, and I'm transparent that scores for never-visited sites are extrapolations."

**"Why not the fancier model / deep learning?"**
"I tested gradient boosting; it didn't beat logistic out-of-fold. In enforcement, an unexplainable score is unusable, so I won't add complexity that doesn't pay for itself."

**"Is 4× real?"**
"It's a cross-validated estimate on public data — directional, not a guarantee. A production pilot with internal FIRE data would confirm it."

**"Privacy / can you even use the text?"**
"Yes, with controls: de-identification, data minimization, in-tenant LLM, access controls, and documented lawful authority. The LLM only structures text — it never assigns enforcement."

**"What would you need to deploy?"**
"Access to FIRE data, an Azure OpenAI deployment in-boundary, a Databricks job for monthly scoring, and a Power BI surface for planners — plus a governance sign-off on fairness and privacy."

**"How often does it run / update?"**
"Monthly scoring is plenty for inspection planning, with model retraining and a fairness/drift check on a regular cadence."

---

## Rehearsal checklist
- [ ] Run through twice out loud, timed (target 8–9 min)
- [ ] Can state the **target** and **selection bias** without notes
- [ ] Know your **two numbers cold**: 4× lift, 32% vs 8%
- [ ] Practice the privacy + human-in-the-loop close — it's what lands for gov leaders
- [ ] Have the appendix slides ready but hidden
