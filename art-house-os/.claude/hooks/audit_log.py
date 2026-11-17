#!/usr/bin/env python3
"""PostToolUse hook: append every MCP call (tool, input summary, timestamp) to data/audit.log."""
import datetime
import json
import os
import sys

event = json.load(sys.stdin)
entry = {
    "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "tool": event.get("tool_name"),
    "input": json.dumps(event.get("tool_input", {}))[:500],
    "session": event.get("session_id"),
}
path = os.path.join(os.environ.get("CLAUDE_PROJECT_DIR", "."), "data", "audit.log")
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "a", encoding="utf-8") as f:
    f.write(json.dumps(entry) + "\n")
