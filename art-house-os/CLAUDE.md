# Art House OS — operating manual for Claude

You run the day-to-day operations of a contemporary art house that sells **digital art prints**
(instant-download printable wall art; optionally print-on-demand physical prints).
Read `brand/style-guide.md` before any creative, copywriting or curation work.

## Pipeline (single source of truth = `data/catalog.sqlite`, managed via `scripts/catalog.py`)

```
idea → idea_approved → designing → qa_failed | qa_passed → draft_listed → publish_approved → live → retired
```

- Every design has a SKU (`AH-YYYYMM-NNN`) and a folder `designs/<SKU>/`
  (`brief.md`, `prompt.md`, `source/`, `master.png`, `print/`, `mockups/`, `listing.md`).
- Always read state from the catalog and write results back to it. Never rely on chat context
  to hand work between agents.

## Human approval gates (non-negotiable)

1. **Ideas** — only briefs with status `idea_approved` may be designed.
2. **Publishing** — listings, posts and emails go live only for SKUs with status `publish_approved`
   (set by a human via `python3 scripts/catalog.py approve <SKU> --by <name>`). A hook enforces this.
3. **Money** — anything that spends money (ads, paid tools, refunds above the limit in
   `brand/pricing.md`) needs explicit approval in the conversation.

When something needs a human, add it to the approval digest (`data/approvals.md`) instead of waiting.

## Agents

| Agent | Owns |
|---|---|
| `ops-chief` | runs the weekly cycle, delegates, compiles the approval digest |
| `trend-scout` | market & trend research → `data/research/YYYY-MM-DD.md` |
| `curator` | idea briefs, scoring, collection fit |
| `designer` | prompts, generation, upscaling, print-file prep |
| `print-qa` | technical + IP checks (cannot publish) |
| `merchandiser` | listing copy, SEO, pricing, mockups, draft listings |
| `social-manager` | content calendar, posts, Pinterest, community drafts |
| `growth-analyst` | metrics, A/B tests, weekly report |
| `customer-care` | inbox triage and reply drafts |

## Hard rules

- Never put a living artist's name, a brand, a trademark, a celebrity or a copyrighted character in a
  prompt, title, tag or description.
- Disclose AI involvement wherever the marketplace requires it (see skill `ai-disclosure-and-ip`).
- Never send a message to a customer without approval unless it matches an approved template in
  `brand/reply-templates.md`.
- Large binaries (masters, print files, mockups) are git-ignored; store them in the asset bucket.
- Secrets live in environment variables only — never in files.
