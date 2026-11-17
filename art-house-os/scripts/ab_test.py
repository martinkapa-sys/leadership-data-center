#!/usr/bin/env python3
"""A/B test helper.

Plan:     ab_test.py plan --baseline 0.02 --mde 0.20 [--alpha 0.05 --power 0.8]
          -> visitors needed per variant to detect a relative lift of --mde over --baseline
Analyse:  ab_test.py analyse --a 1200,24 --b 1180,35 [--ship 0.95 --min-trials 500]
          -> Bayesian Beta(1,1) posterior: P(B > A), expected lift, 90% credible interval, decision
Catalog:  ab_test.py analyse --experiment ID   (reads trials/conversions from data/catalog.sqlite)
"""
import argparse
import os
import random
import sqlite3
from statistics import NormalDist

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "catalog.sqlite")


def plan(a):
    p1 = a.baseline
    p2 = p1 * (1 + a.mde)
    z = NormalDist()
    za, zb = z.inv_cdf(1 - a.alpha / 2), z.inv_cdf(a.power)
    pbar = (p1 + p2) / 2
    n = ((za * (2 * pbar * (1 - pbar)) ** 0.5 + zb * (p1 * (1 - p1) + p2 * (1 - p2)) ** 0.5) ** 2) / (p2 - p1) ** 2
    print(f"Baseline {p1:.2%} -> {p2:.2%} (+{a.mde:.0%} relative): need ~{int(n) + 1} visitors per variant "
          f"({2 * (int(n) + 1)} total) at alpha={a.alpha}, power={a.power}.")


def analyse_counts(ta, ca, tb, cb, ship, min_trials, draws=200_000, seed=7):
    rng = random.Random(seed)
    wins, lifts = 0, []
    for _ in range(draws):
        pa = rng.betavariate(1 + ca, 1 + ta - ca)
        pb = rng.betavariate(1 + cb, 1 + tb - cb)
        wins += pb > pa
        lifts.append(pb / pa - 1)
    lifts.sort()
    prob = wins / draws
    if min(ta, tb) < min_trials:
        decision = f"CONTINUE — need at least {min_trials} trials per variant"
    elif prob >= ship:
        decision = "SHIP B"
    elif prob <= 1 - ship:
        decision = "KEEP A (kill B)"
    else:
        decision = "CONTINUE — inconclusive"
    return {
        "rate_a": ca / ta, "rate_b": cb / tb, "p_b_beats_a": prob,
        "expected_lift": sum(lifts) / draws,
        "ci90": (lifts[int(0.05 * draws)], lifts[int(0.95 * draws)]),
        "decision": decision,
    }


def analyse(a):
    if a.experiment:
        con = sqlite3.connect(DB)
        rows = con.execute("SELECT variant, trials, conversions FROM experiment_results WHERE experiment_id=? "
                           "ORDER BY variant", (a.experiment,)).fetchall()
        if len(rows) != 2:
            raise SystemExit(f"Experiment {a.experiment} needs exactly 2 variants with results, found {len(rows)}")
        (_, ta, ca), (_, tb, cb) = rows
    else:
        ta, ca = (int(x) for x in a.a.split(","))
        tb, cb = (int(x) for x in a.b.split(","))
    r = analyse_counts(ta, ca, tb, cb, a.ship, a.min_trials)
    print(f"A: {ca}/{ta} = {r['rate_a']:.2%}   B: {cb}/{tb} = {r['rate_b']:.2%}")
    print(f"P(B > A) = {r['p_b_beats_a']:.1%}   expected lift {r['expected_lift']:+.1%}   "
          f"90% CI [{r['ci90'][0]:+.1%}, {r['ci90'][1]:+.1%}]")
    print(f"Decision: {r['decision']}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("plan")
    s.add_argument("--baseline", type=float, required=True)
    s.add_argument("--mde", type=float, required=True, help="minimum detectable relative lift, e.g. 0.2")
    s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--power", type=float, default=0.8)
    s = sub.add_parser("analyse")
    s.add_argument("--a"); s.add_argument("--b"); s.add_argument("--experiment", type=int)
    s.add_argument("--ship", type=float, default=0.95)
    s.add_argument("--min-trials", type=int, default=500)
    a = p.parse_args()
    plan(a) if a.cmd == "plan" else analyse(a)


if __name__ == "__main__":
    main()
