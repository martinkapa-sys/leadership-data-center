---
name: ab-test-design
description: Design an A/B test before running it: hypothesis, metric, sample size, duration, stopping rule. Use before any experiment.
---
1. Hypothesis: "Changing <X> for <SKUs/audience> will raise <metric> because <reason>."
2. Primary metric (one): CTR (ads/pins), visit→order conversion, AOV, revenue per visitor.
3. Sample size: `python3 scripts/ab_test.py plan --baseline <rate> --mde <relative lift>`. If it needs more traffic than ~4 weeks gives, test something bigger or use ads.
4. Where to test:
   - **Ad creative** (Meta/Pinterest ads): mockups, hooks, themes — fastest, cleanest split.
   - **Shopify** with an A/B app: price, page layout, hero image.
   - **Etsy**: no native split — run sequential tests (2–4 weeks each) on comparable listings and treat results as weaker evidence.
5. Register: `python3 scripts/catalog.py experiment-add --name ... --hypothesis ... --metric ... --variants A,B --sku ...`
6. Stopping rule: decide only after min trials per variant (default 500) using `ab-test-analysis`. No peeking-based early stops.
