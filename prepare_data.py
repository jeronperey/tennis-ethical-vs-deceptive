"""Data processing for Assignment 3 (kept separate from the visualization code).

Reads Jeff Sackmann's ATP match files (2015-2024), applies the exclusions below in
order, and writes the small CSVs the charts use. Run:  python3 prepare_data.py
Source: Jeff Sackmann, Tennis Abstract (CC BY-NC-SA 4.0),
via github.com/Aneeshers/tennis-sackmann-archive.
"""
import csv, glob, os

HERE = os.path.dirname(os.path.abspath(__file__))
SURFACES = {"Hard", "Clay", "Grass"}
UNFINISHED = ("RET", "W/O", "DEF", "ABD", "UNP")  # retirements, walkovers, defaults (from the score text)
BINS = [("1-2", 1, 2), ("3-5", 3, 5), ("6-9", 6, 9), ("10+", 10, 10**9)]

def bin_of(gap):
    return next(name for name, lo, hi in BINS if lo <= gap <= hi)

rows, audit = [], {"total": 0, "other_surface": 0, "unfinished": 0, "missing_aces": 0, "tied_aces": 0}
for path in sorted(glob.glob(os.path.join(HERE, "data", "raw", "atp_matches_20*.csv"))):
    for r in csv.DictReader(open(path, newline="", encoding="utf-8")):
        audit["total"] += 1
        if r["surface"] not in SURFACES:                       # 1. other or missing surface (e.g. carpet)
            audit["other_surface"] += 1; continue
        if any(k in r["score"].upper() for k in UNFINISHED):   # 2. unfinished match ("Def." is mixed case)
            audit["unfinished"] += 1; continue
        if not r["w_ace"] or not r["l_ace"]:                   # 3. missing ace counts
            audit["missing_aces"] += 1; continue
        wa, la = int(float(r["w_ace"])), int(float(r["l_ace"]))
        if wa == la:                                           # 4. tied ace counts
            audit["tied_aces"] += 1; continue
        rows.append({"year": r["tourney_date"][:4], "surface": r["surface"], "ace_advantage": abs(wa - la),
                     "higher_ace_player_won": int(wa > la)})   # the winner out-aced the loser

for r in rows:
    r["ace_advantage_bin"] = bin_of(r["ace_advantage"])

out = os.path.join(HERE, "data", "processed")
with open(os.path.join(out, "ace_advantage_win_rates.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ace_advantage_bin", "higher_ace_won", "matches", "win_pct"])
    for name, _, _ in BINS:
        g = [r for r in rows if r["ace_advantage_bin"] == name]
        won = sum(r["higher_ace_player_won"] for r in g)
        w.writerow([name, won, len(g), round(100 * won / len(g), 2)])
with open(os.path.join(out, "audit.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["step", "matches"])
    for k, v in audit.items(): w.writerow([k, v])
    w.writerow(["analyzed", len(rows)])
print(audit, "analyzed:", len(rows))

# Small JS file so the static charts can load their data without a server (file:// blocks fetch).
import json
bins = list(csv.DictReader(open(os.path.join(out, "ace_advantage_win_rates.csv"))))
payload = {"bins": [{"bin": b["ace_advantage_bin"], "won": int(b["higher_ace_won"]), "n": int(b["matches"]),
                     "pct": float(b["win_pct"])} for b in bins],
           "audit": {**audit, "analyzed": len(rows)}}
open(os.path.join(HERE, "data.js"), "w").write("const DATA = " + json.dumps(payload, indent=2) + ";\n")
