# Art House OS

A Claude Code setup that runs a contemporary art house selling digital prints:
market research → idea briefs → design → print QA → listings → social → analytics → A/B tests → back to research.

> This folder lives inside `leadership-data-center` only because the session could not create a new
> repository. Move it to its own repo (`art-house-os`) — Claude Code reads `.claude/`, `CLAUDE.md` and
> `.mcp.json` from the project root, and GitHub only runs workflows from the root `.github/`.

## Quick start

```bash
pip install -r requirements.txt
python3 scripts/catalog.py init
cp .env.example .env            # fill in keys, then load them into your shell / environment secrets
claude                          # then: "use the ops-chief agent to run this week's cycle"
```

1. Fill in `brand/style-guide.md`, `brand/pricing.md` and `brand/reply-templates.md` — this is where your taste lives.
2. Enable connectors (see `docs/connectors.md`) — start with shop + image generation only.
3. Run the pipeline manually for 2 weeks, approving everything. Then schedule it (`docs/scheduling.md`).

## What's here

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Operating manual: pipeline, approval gates, hard rules |
| `.claude/agents/` | 9 role agents with scoped tools |
| `.claude/skills/` | 20 procedures (research, design, QA, SEO, social, A/B, reporting…) |
| `.claude/hooks/` | `require_approval.py` (blocks publishing unapproved SKUs), `audit_log.py` |
| `.claude/settings.json` | permissions + hook wiring |
| `.mcp.json` | connectors with confirmed endpoints |
| `scripts/catalog.py` | catalog/pipeline database CLI |
| `scripts/print_prep.py` | crop/resize master to all print ratios at 300 DPI with sRGB |
| `scripts/print_qa.py` | technical pass/fail checks on print files |
| `scripts/mockup.py` | composite art into room/frame mockup templates |
| `scripts/ab_test.py` | sample-size planning + Bayesian A/B analysis |
| `docs/` | connectors, scheduling, rollout plan |
| `.github/workflows/weekly-cycle.yml` | scheduled weekly cycle via `claude-code-action` |
