---
name: ab-test-analysis
description: Analyse A/B test results and decide ship/kill/continue. Use when evaluating a running or finished experiment.
---
1. Update counts: `python3 scripts/catalog.py experiment-result <id> --variant A --trials N --conversions N` (and B).
2. `python3 scripts/ab_test.py analyse --experiment <id>` → P(B>A), expected lift, 90% credible interval, decision.
3. Ship if P(B>A) ≥ 95% and min trials met; kill if ≤ 5%; otherwise continue until the planned duration, then keep the simpler/cheaper variant.
4. Write the result into the weekly report and update `brand/learnings.md` (what won, by how much, in what context) so future briefs and listings use it.
