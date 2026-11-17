#!/usr/bin/env python3
"""Catalog & pipeline database for Art House OS.

Usage:
  catalog.py init
  catalog.py add-idea --title T --theme TH [--collection C] [--score 0-100] [--brief PATH]
  catalog.py list [--status S]
  catalog.py show SKU
  catalog.py set-status SKU STATUS [--note N]
  catalog.py approve SKU --by NAME [--stage idea|publish]     (humans only)
  catalog.py qa-result SKU --passed|--failed --report PATH
  catalog.py add-listing SKU --channel etsy|shopify|... --url URL [--external-id ID] [--price P]
  catalog.py add-metrics SKU --date YYYY-MM-DD --channel C [--views N] [--visits N] [--favorites N]
                         [--orders N] [--revenue X]
  catalog.py experiment-add --name N --hypothesis H --metric M --variants A,B [--sku SKU]
  catalog.py experiment-result ID --variant V --trials N --conversions N
  catalog.py report [--days 7]
"""
import argparse
import datetime as dt
import json
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "catalog.sqlite")

STATUSES = ["idea", "idea_approved", "idea_rejected", "designing", "qa_failed", "qa_passed",
            "draft_listed", "publish_approved", "live", "retired"]

SCHEMA = """
CREATE TABLE IF NOT EXISTS designs (
  sku TEXT PRIMARY KEY, title TEXT NOT NULL, theme TEXT, collection TEXT,
  score INTEGER, status TEXT NOT NULL DEFAULT 'idea', brief_path TEXT,
  qa_passed INTEGER DEFAULT 0, qa_report TEXT, approved_by TEXT, approved_at TEXT,
  created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT, sku TEXT, kind TEXT, detail TEXT, at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS listings (
  id INTEGER PRIMARY KEY AUTOINCREMENT, sku TEXT NOT NULL, channel TEXT NOT NULL,
  url TEXT, external_id TEXT, price REAL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS metrics (
  sku TEXT NOT NULL, date TEXT NOT NULL, channel TEXT NOT NULL,
  views INTEGER DEFAULT 0, visits INTEGER DEFAULT 0, favorites INTEGER DEFAULT 0,
  orders INTEGER DEFAULT 0, revenue REAL DEFAULT 0,
  PRIMARY KEY (sku, date, channel)
);
CREATE TABLE IF NOT EXISTS experiments (
  id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, sku TEXT, hypothesis TEXT, metric TEXT,
  variants TEXT, status TEXT DEFAULT 'running', decision TEXT, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS experiment_results (
  experiment_id INTEGER, variant TEXT, trials INTEGER, conversions INTEGER, updated_at TEXT,
  PRIMARY KEY (experiment_id, variant)
);
"""


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def connect() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def log(con, sku, kind, detail=""):
    con.execute("INSERT INTO events (sku, kind, detail, at) VALUES (?,?,?,?)", (sku, kind, detail, now()))


def require(con, sku):
    row = con.execute("SELECT * FROM designs WHERE sku=?", (sku,)).fetchone()
    if row is None:
        sys.exit(f"Unknown SKU {sku}")
    return row


def next_sku(con) -> str:
    prefix = "AH-" + dt.date.today().strftime("%Y%m") + "-"
    row = con.execute("SELECT sku FROM designs WHERE sku LIKE ? ORDER BY sku DESC LIMIT 1", (prefix + "%",)).fetchone()
    n = int(row["sku"][-3:]) + 1 if row else 1
    return f"{prefix}{n:03d}"


def cmd_init(con, a):
    con.executescript(SCHEMA)
    print(f"Initialised {DB}")


def cmd_add_idea(con, a):
    sku = next_sku(con)
    con.execute("INSERT INTO designs (sku,title,theme,collection,score,brief_path,created_at,updated_at) "
                "VALUES (?,?,?,?,?,?,?,?)", (sku, a.title, a.theme, a.collection, a.score, a.brief, now(), now()))
    os.makedirs(os.path.join(ROOT, "designs", sku), exist_ok=True)
    log(con, sku, "created", a.title)
    print(sku)


def cmd_list(con, a):
    q, args = "SELECT sku,status,score,collection,title FROM designs", []
    if a.status:
        q += " WHERE status=?"
        args.append(a.status)
    for r in con.execute(q + " ORDER BY sku", args):
        print(f"{r['sku']}  {r['status']:<16} {str(r['score'] or ''):>3}  {r['collection'] or '-':<18} {r['title']}")


def cmd_show(con, a):
    r = require(con, a.sku)
    out = dict(r)
    out["listings"] = [dict(x) for x in con.execute("SELECT * FROM listings WHERE sku=?", (a.sku,))]
    out["events"] = [dict(x) for x in con.execute("SELECT kind,detail,at FROM events WHERE sku=? ORDER BY id", (a.sku,))]
    print(json.dumps(out, indent=2))


def cmd_set_status(con, a):
    require(con, a.sku)
    if a.status not in STATUSES:
        sys.exit(f"Status must be one of {STATUSES}")
    if a.status in ("idea_approved", "publish_approved"):
        sys.exit("Use `approve` for approval statuses — they are reserved for humans.")
    if a.status == "draft_listed" and not require(con, a.sku)["qa_passed"]:
        sys.exit("Cannot list a design that has not passed QA.")
    con.execute("UPDATE designs SET status=?, updated_at=? WHERE sku=?", (a.status, now(), a.sku))
    log(con, a.sku, "status", f"{a.status} {a.note or ''}".strip())
    print(f"{a.sku} -> {a.status}")


def cmd_approve(con, a):
    r = require(con, a.sku)
    if a.stage == "idea":
        if r["status"] != "idea":
            sys.exit(f"{a.sku} is '{r['status']}', expected 'idea'")
        con.execute("UPDATE designs SET status='idea_approved', updated_at=? WHERE sku=?", (now(), a.sku))
    else:
        if r["status"] != "draft_listed" or not r["qa_passed"]:
            sys.exit(f"{a.sku} is '{r['status']}' (qa_passed={r['qa_passed']}); must be draft_listed and QA-passed")
        con.execute("UPDATE designs SET status='publish_approved', approved_by=?, approved_at=?, updated_at=? "
                    "WHERE sku=?", (a.by, now(), now(), a.sku))
    log(con, a.sku, f"approved_{a.stage}", a.by)
    print(f"{a.sku} approved for {a.stage} by {a.by}")


def cmd_qa_result(con, a):
    require(con, a.sku)
    status = "qa_passed" if a.passed else "qa_failed"
    con.execute("UPDATE designs SET qa_passed=?, qa_report=?, status=?, updated_at=? WHERE sku=?",
                (1 if a.passed else 0, a.report, status, now(), a.sku))
    log(con, a.sku, "qa", f"{status} {a.report}")
    print(f"{a.sku} -> {status}")


def cmd_add_listing(con, a):
    require(con, a.sku)
    con.execute("INSERT INTO listings (sku,channel,url,external_id,price,created_at) VALUES (?,?,?,?,?,?)",
                (a.sku, a.channel, a.url, a.external_id, a.price, now()))
    log(con, a.sku, "listing", f"{a.channel} {a.url}")
    print("ok")


def cmd_add_metrics(con, a):
    require(con, a.sku)
    con.execute("INSERT OR REPLACE INTO metrics VALUES (?,?,?,?,?,?,?,?)",
                (a.sku, a.date, a.channel, a.views, a.visits, a.favorites, a.orders, a.revenue))
    print("ok")


def cmd_experiment_add(con, a):
    cur = con.execute("INSERT INTO experiments (name,sku,hypothesis,metric,variants,created_at) VALUES (?,?,?,?,?,?)",
                      (a.name, a.sku, a.hypothesis, a.metric, a.variants, now()))
    print(cur.lastrowid)


def cmd_experiment_result(con, a):
    con.execute("INSERT OR REPLACE INTO experiment_results VALUES (?,?,?,?,?)",
                (a.id, a.variant, a.trials, a.conversions, now()))
    print("ok")


def cmd_report(con, a):
    since = (dt.date.today() - dt.timedelta(days=a.days)).isoformat()
    print(f"# KPI report — last {a.days} days (since {since})\n")
    tot = con.execute("SELECT SUM(views) v, SUM(visits) s, SUM(orders) o, SUM(revenue) r FROM metrics WHERE date>=?",
                      (since,)).fetchone()
    v, s, o, r = (tot["v"] or 0), (tot["s"] or 0), (tot["o"] or 0), (tot["r"] or 0.0)
    print(f"Views {v} | Visits {s} | Orders {o} | Revenue {r:.2f} | "
          f"Conversion {o / s:.2%} | AOV {(r / o if o else 0):.2f}\n" if s else "No traffic data.\n")
    print("## Top SKUs by revenue")
    for x in con.execute("SELECT m.sku, d.title, SUM(orders) o, SUM(revenue) r, SUM(visits) s FROM metrics m "
                         "JOIN designs d USING (sku) WHERE date>=? GROUP BY m.sku ORDER BY r DESC LIMIT 10", (since,)):
        print(f"- {x['sku']} {x['title']}: {x['o']} orders, {x['r']:.2f} revenue, {x['s']} visits")
    print("\n## Pipeline")
    for x in con.execute("SELECT status, COUNT(*) n FROM designs GROUP BY status ORDER BY status"):
        print(f"- {x['status']}: {x['n']}")
    print("\n## Running experiments")
    for x in con.execute("SELECT id, name, metric FROM experiments WHERE status='running'"):
        print(f"- #{x['id']} {x['name']} ({x['metric']})")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    s = sub.add_parser("add-idea"); s.add_argument("--title", required=True); s.add_argument("--theme")
    s.add_argument("--collection"); s.add_argument("--score", type=int); s.add_argument("--brief")
    s = sub.add_parser("list"); s.add_argument("--status")
    s = sub.add_parser("show"); s.add_argument("sku")
    s = sub.add_parser("set-status"); s.add_argument("sku"); s.add_argument("status"); s.add_argument("--note")
    s = sub.add_parser("approve"); s.add_argument("sku"); s.add_argument("--by", required=True)
    s.add_argument("--stage", choices=["idea", "publish"], default="publish")
    s = sub.add_parser("qa-result"); s.add_argument("sku"); s.add_argument("--report", required=True)
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--passed", action="store_true"); g.add_argument("--failed", action="store_true")
    s = sub.add_parser("add-listing"); s.add_argument("sku"); s.add_argument("--channel", required=True)
    s.add_argument("--url"); s.add_argument("--external-id"); s.add_argument("--price", type=float)
    s = sub.add_parser("add-metrics"); s.add_argument("sku"); s.add_argument("--date", required=True)
    s.add_argument("--channel", required=True)
    for f in ("views", "visits", "favorites", "orders"):
        s.add_argument(f"--{f}", type=int, default=0)
    s.add_argument("--revenue", type=float, default=0.0)
    s = sub.add_parser("experiment-add"); s.add_argument("--name", required=True)
    s.add_argument("--hypothesis", required=True); s.add_argument("--metric", required=True)
    s.add_argument("--variants", required=True); s.add_argument("--sku")
    s = sub.add_parser("experiment-result"); s.add_argument("id", type=int); s.add_argument("--variant", required=True)
    s.add_argument("--trials", type=int, required=True); s.add_argument("--conversions", type=int, required=True)
    s = sub.add_parser("report"); s.add_argument("--days", type=int, default=7)
    a = p.parse_args()

    con = connect()
    if a.cmd != "init":
        con.executescript(SCHEMA)
    globals()["cmd_" + a.cmd.replace("-", "_")](con, a)
    con.commit()


if __name__ == "__main__":
    main()
