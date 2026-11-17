#!/usr/bin/env python3
"""PreToolUse hook: block outward-facing MCP actions for SKUs a human has not approved.

A tool call counts as "publishing" when its name contains one of PUBLISH_VERBS
(e.g. mcp__shopify__create_product, mcp__pinterest__create_pin).
Such calls must reference a SKU (AH-YYYYMM-NNN) anywhere in their input, and every
referenced SKU must be in status `publish_approved` or `live` with `approved_by` set.
Exit code 2 blocks the call and shows stderr to Claude.
"""
import json
import os
import re
import sqlite3
import sys

# Servers whose write actions put content in front of customers. Gmail/Slack/Calendar are not gated here
# (they go through permission prompts and reply templates instead).
GATED_SERVERS = ("shopify", "etsy", "printful", "gelato", "printify", "pinterest", "meta", "buffer", "klaviyo")
PUBLISH_VERBS = ("publish", "create_product", "update_product", "create_listing", "update_listing",
                 "activate", "create_pin", "create_post", "schedule", "send", "campaign")
SKU_RE = re.compile(r"\bAH-\d{6}-\d{3}\b")


def main() -> int:
    event = json.load(sys.stdin)
    tool = event.get("tool_name", "")
    name = tool.lower()
    parts = name.split("__")
    if len(parts) < 3 or parts[1] not in GATED_SERVERS or not any(v in parts[2] for v in PUBLISH_VERBS):
        return 0

    payload = json.dumps(event.get("tool_input", {}))
    skus = sorted(set(SKU_RE.findall(payload)))
    if not skus:
        print(f"Blocked {tool}: publishing actions must reference the catalog SKU (AH-YYYYMM-NNN) "
              "in their input (e.g. as a tag, SKU field or metadata) so approval can be checked.",
              file=sys.stderr)
        return 2

    db = os.path.join(os.environ.get("CLAUDE_PROJECT_DIR", "."), "data", "catalog.sqlite")
    if not os.path.exists(db):
        print("Blocked: data/catalog.sqlite missing — run `python3 scripts/catalog.py init`.", file=sys.stderr)
        return 2
    con = sqlite3.connect(db)
    problems = []
    for sku in skus:
        row = con.execute("SELECT status, approved_by FROM designs WHERE sku = ?", (sku,)).fetchone()
        if row is None:
            problems.append(f"{sku}: not in catalog")
        elif row[0] not in ("publish_approved", "live") or not row[1]:
            problems.append(f"{sku}: status '{row[0]}', approved_by={row[1]!r}")
    if problems:
        print(f"Blocked {tool} — human approval missing:\n  " + "\n  ".join(problems) +
              "\nAdd the SKU to data/approvals.md and wait for "
              "`python3 scripts/catalog.py approve <SKU> --by <name>`.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
