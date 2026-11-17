---
name: trend-research
description: Weekly market and trend research for digital wall art: sources, scoring of demand vs competition, report format. Use when scanning trends or validating a niche.
---
## Sources (check each, cite links)
1. **Etsy search**: autocomplete suggestions for seed terms ("printable wall art", "<room> print", "<style> poster"); results count = competition; bestseller badges and review counts on page 1 = demand. Apify Etsy scraper actor for bulk pulls.
2. **Pinterest Trends** (trends.pinterest.com) and Pinterest search autocomplete for home decor — leading indicator 1–3 months ahead.
3. **Google Trends**: 12-month and 5-year curves for candidate themes; note seasonality peaks.
4. **Instagram/TikTok**: hashtag volume and recent top posts for #wallart, #gallerywall, #printableart, room-style tags.
5. **Interior design press / paint colour of the year / furniture retailers' new collections** — palettes and styles.
6. **Competitor shops** in `brand/competitors.md` (see `competitor-teardown`).

## Scoring each opportunity
- Demand 1–5: search trend direction, Pinterest interest, review velocity of top listings.
- Competition 1–5 (5 = crowded): results count, quality of top 10, how many big shops dominate.
- Opportunity = demand × (6 − competition); flag ≥ 15.
- Lead time: listings need ~4–8 weeks to rank — favour themes peaking 6–10 weeks out.

## Output
`data/research/YYYY-MM-DD.md` using the structure in the trend-scout agent. Compare with the previous report and mark ↑/↓/new.
