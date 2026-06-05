# Concept Log

> Lightweight scratchpad for things you learned in **concept explainer chats**.  
> Not every question needs an entry — only concepts you'll reuse or might get interviewed on.

**Difference from decision_log:**
- **decision_log** = "I chose X over Y because…" (commitments)
- **concept_log** = "I now understand what X means" (learning)

---

## Template

```
### [Concept name]
**Date:** YYYY-MM-DD  
**One-line definition:**  
**Why it matters for this project:**  
**Example in our data:**  
**Source:** (chat / article / notebook)
```

---

## Entries

*(Add as you learn)*

### Selection bias
**Date:** 2026-06-05  
**One-line definition:** Training labels come from a non-random subset of workplaces (those inspected), so the model learns "who we inspect" as well as "who is risky."  
**Why it matters:** Core limitation of this entire project; must say in interview.  
**Example:** A workplace never inspected has no order history — looks low risk by default.  
**Source:** Master chat / 01_SOLUTION

### Temporal leakage
**Date:** 2026-06-05  
**One-line definition:** Using information from the future to predict the past (e.g. random split on time-series data).  
**Why it matters:** Inflates metrics; invalidates out-of-time claims.  
**Example:** Including 2023 orders in features when predicting 2023 outcomes.  
**Source:** Master chat

### Lift (top decile)
**Date:** 2026-06-05  
**One-line definition:** How much better the model's top-scored group performs vs the overall base rate.  
**Why it matters:** Business metric — "serious findings per inspection if we target top 10%."  
**Example:** If 5% of workplaces have serious orders overall but 15% in top decile → lift = 3×.  
**Source:** Master chat
