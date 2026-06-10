# Design Notes — MLITSD Risk Identification Deck

**Fonts**
- Headers/titles & key stats: **Cambria** (serif, ships with Office, professional)
- Body, bullets, captions: **Calibri** (sans, ships with Office)
- JSON / code blocks: **Courier New** (monospace)
- All three are metric-safe, so what you see in the file matches what renders on the panel's PowerPoint.

**Color palette (hex)**
| Role | Hex | Use |
|---|---|---|
| Navy (dominant) | `1F3A5F` | Titles, primary cards, callout #1 |
| Dark navy | `16263D` | Title slide bg, JSON code blocks |
| Blue (supporting) | `2E5C8A` | Secondary emphasis, "32%" stat |
| Steel | `5B7FA6` | Arrows, kicker accents on dark |
| Gold (accent, restrained) | `C8A24B` | Section kickers, the "4×" stat, roadmap nodes |
| Body grey | `5A6470` | Body text |
| Muted grey | `8A929C` | Captions |
| Card tints | `EEF3F8` / `F4F7FA` | Card backgrounds |
| Background | `FFFFFF` | Content slides |

Blue + grey government palette as required; gold is used sparingly as a single sharp accent for the two headline numbers and section kickers, not as decoration.

**Layout / motif**
- Slide 1 (title) and the JSON blocks use the dark navy for a "sandwich" anchor; content slides are white.
- Repeating motif: icons in solid navy circles + soft rounded cards with subtle shadow. No accent stripes or underlines.
- Layouts deliberately vary: title + funnel (S1), 5-step pipeline (S2), two-panel chart/text (S3), chart + stat callouts (S4), icon rows + vertical timeline (S5).

**Chart placement (as specified in the prompt)**
- `feature_importance.png` → Slide 3, left panel (scaled to 5.35" wide, aspect-preserved from 1200×750).
- `lift_chart.png` → Slide 4, left panel (scaled to ~6.95" wide, aspect-preserved).
- Charts embedded directly from the provided PNGs — no recreation, numbers untouched.

**Slide 3 right panel** — the LLM before→after was recreated as a visual (de-identified excerpt → schema-constrained JSON) per Section 3 of the prompt, with the "text adds what structured fields miss" framing.

**Assumptions made**
- 16:9 widescreen (LAYOUT_WIDE, 13.3"×7.5").
- The JSON on Slide 3 omits the `Reg 851 s.7` citation for space (shows `…`); the full schema appears on Appendix A4.
- Appendix slides A1–A4 are included after the 5 main slides and labeled "APPENDIX — BACKUP FOR Q&A"; they do not count toward the 5-slide limit. If the panel wants exactly 5 slides visible, delete or hide slides 6–9 before presenting.
- Speaker notes are attached to all 5 main slides (Presenter View); the standalone `Speaker_Script.md` carries the full timed script + Q&A + checklist.
