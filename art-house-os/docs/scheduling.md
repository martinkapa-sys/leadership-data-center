# Operating cadence

| When | Agent(s) | Prompt |
|---|---|---|
| Mon 07:10 | ops-chief → trend-scout → curator | "Run the Monday research cycle and write the approval digest." |
| Daily 08:20 | ops-chief → designer, print-qa, merchandiser | "Advance every approved idea and QA-passed design one stage; update the digest." |
| Daily 12:40 | social-manager | "Publish today's calendar items for live SKUs and draft community replies." |
| Daily 16:15 | customer-care | "Triage new messages and draft replies." |
| Fri 15:30 | growth-analyst | "Pull this week's metrics, evaluate experiments, write the weekly report." |
| 1st of month | ops-chief + curator | "Monthly collection review: retire weak SKUs, plan bundles and the next season." |

## How to run them
- **Claude Code cloud scheduled tasks** (claude.ai/code): create one per row with the prompt above. Simplest option.
- **GitHub Actions**: `.github/workflows/weekly-cycle.yml` (move this folder to its own repo root first).
- **Local**: `/loop` inside a running session, or cron + `claude -p "<prompt>"`.

## Your part (≈20 min/day)
Read `data/approvals.md`, then approve:
```
python3 scripts/catalog.py approve <SKU> --stage idea --by <you>      # ideas
python3 scripts/catalog.py approve <SKU> --by <you>                   # publishing
```
