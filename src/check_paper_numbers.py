"""
check_paper_numbers.py -- recompute the headline numbers of the paper from the
stored test outputs in results/paper_v1/. CPU only, no model, no GSM8K download.

    cd src
    python check_paper_numbers.py                       # default: ../results/paper_v1
    python check_paper_numbers.py --paper-dir <dir>

What it checks, and where each number appears in the paper
-----------------------------------------------------------
  1. probe verdicts on the 847 testable traces           Table "probe verdicts"
  2. refutation rate by failure type                     Figure "per-type detection"
  3. end-to-end accuracy of every policy (McNemar)       Table "all policies"
  4. flag precision, repair rate R, damage rate D,
     break-even precision D/(R+D) and the net change     Section "accounting identity"
  5. detection AUROC of p_wrong, the probe, and their
     blend over a grid of weights                        Section "support and refutation"
  6. the training-split calibration table                Appendix "detector calibration"

Correctness labels come from mpv_per_question.jsonl, which score_mpv.py wrote
after opening the reference answers once, at the end of the run.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


def auroc(scores, labels):
    """labels: 1 = wrong. Rank-based with tie correction (same as blend_check.py)."""
    pairs = sorted(zip(scores, labels))
    n_pos = sum(labels)
    n_neg = len(labels) - n_pos
    ranks = [0.0] * len(pairs)
    i = 0
    while i < len(pairs):
        j = i
        while j + 1 < len(pairs) and pairs[j + 1][0] == pairs[i][0]:
            j += 1
        for k in range(i, j + 1):
            ranks[k] = (i + j) / 2.0 + 1.0
        i = j + 1
    s_pos = sum(r for r, (_, y) in zip(ranks, pairs) if y == 1)
    return (s_pos - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


def jsonl(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper-dir", default=str(HERE.parent / "results" / "paper_v1"))
    ap.add_argument("--skip-blend", action="store_true",
                    help="skip the AUROC grid (it re-executes every trace program, ~1-2 min)")
    a = ap.parse_args()
    test = Path(a.paper_dir) / "test"
    rep = json.load(open(test / "mpv_report.json"))
    pq = {d["id"]: d for d in jsonl(test / "mpv_per_question.jsonl")}
    rows = jsonl(test / "results.jsonl")

    probe_rows = jsonl(test / "mpv_probes.jsonl")
    print("=" * 72)
    print(f"  Probe coverage: {len(probe_rows)} probes over "
          f"{len({d['id'] for d in probe_rows})} of {len(rows)} test questions")
    rs = rep.get("reasons", {})
    print(f"  Questions decided by probe evidence: {rs.get('metamorphic', 0) + rs.get('program', 0)}")
    print("\n  1. Probe verdicts on testable pass-1 traces")
    sp = rep["support_precision"]
    n_s, c_s, n_r, c_r = sp["supported_n"], sp["supported_correct"], sp["refuted_n"], sp["refuted_correct"]
    n = n_s + n_r
    print(f"     supported {n_s:4d}  correct {c_s:4d}  P(correct) {c_s/n_s:6.1%}")
    print(f"     refuted   {n_r:4d}  correct {c_r:4d}  P(correct) {c_r/n_r:6.1%}")
    print(f"     all       {n:4d}  correct {c_s+c_r:4d}  base rate  {(c_s+c_r)/n:6.1%}")
    w_s, w_r = n_s - c_s, n_r - c_r
    print(f"     odds ratio {(c_s*w_r)/(w_s*c_r):.2f}")
    try:
        from scipy.stats import fisher_exact
        print(f"     Fisher p   {fisher_exact([[c_s, w_s], [c_r, w_r]])[1]:.2g}")
    except ImportError:
        print("     (install scipy for the Fisher test)")

    print("\n  2. Refutation rate by failure type")
    for t, d in rep["refuted_by_type"].items():
        print(f"     {t:13s} {d['refuted']:4d}/{d['n']:<4d} {d['refuted']/d['n']:6.1%}")

    print("\n  3. End-to-end accuracy, paired McNemar against pass-1")
    for arm in ("pass1", "replace", "replace_mpv_veto", "select_symbolic",
                "select_mpv", "select_mpv_backsub"):
        d = rep[arm]
        p = d.get("vs_pass1", {}).get("p")
        print(f"     {arm:20s} {d['correct']:4d}/{d['n']}  {d['acc']:7.2%}"
              + (f"   p = {p:.3f}" if arm != "pass1" else ""))

    ys_all = [0 if pq[r["id"]]["pass1"] else 1 for r in rows]
    print(f"\n  Static detector on all {len(rows)} test questions: AUROC "
          f"{auroc([float(r['p_wrong']) for r in rows], ys_all):.3f}")

    print("\n  4. Flags, repair and damage on test")
    flagged = [r for r in rows if r.get("flagged")]
    tp = [r for r in flagged if pq[r["id"]]["pass1"] is False]
    fp = [r for r in flagged if pq[r["id"]]["pass1"] is True]
    rep_ = sum(1 for r in tp if pq[r["id"]]["retry"] is True)
    dmg = sum(1 for r in fp if pq[r["id"]]["retry"] is False)
    R, D = rep_ / len(tp), dmg / len(fp)
    print(f"     flagged {len(flagged)} ({len(flagged)/len(rows):.1%}), wrong {len(tp)}, correct {len(fp)},"
          f" precision {len(tp)/len(flagged):.1%}")
    print(f"     repaired {rep_}/{len(tp)} (R = {R:.1%}), damaged {dmg}/{len(fp)} (D = {D:.1%})")
    print(f"     break-even precision D/(R+D) = {D/(R+D):.1%}; net change {rep_ - dmg:+d}")

    if not a.skip_blend:
        print("\n  5. Detection AUROC on the testable traces (re-executes each trace program)")
        import sys
        sys.path.insert(0, str(HERE))
        import mpv
        from extraction import extract_final_answer
        probes = defaultdict(dict)
        for d in jsonl(test / "mpv_probes.jsonl"):
            if d.get("model_answer") is None:
                continue
            key = (round(float(d["target_value"]), 6), round(float(d["new_value"]), 6))
            probes[d["id"]][key] = mpv.Probe.from_dict(d)
        data = []
        for r in rows:
            pr = [probes[r["id"]][k] for k in sorted(probes.get(r["id"], {}))]
            if not pr or r.get("p_wrong") is None:
                continue
            ms = mpv.detection_score(r["question"], r["trace"], extract_final_answer(r["trace"]), pr)
            if ms is None:
                continue
            data.append((ms, float(r["p_wrong"]), 0 if pq[r["id"]]["pass1"] else 1))
        ys = [y for *_, y in data]
        print(f"     n = {len(data)} ({sum(ys)} wrong)")
        print(f"     probe alone    {auroc([m for m, _, _ in data], ys):.3f}")
        print(f"     p_wrong alone  {auroc([p for _, p, _ in data], ys):.3f}")
        for w in (0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 0.9):
            tag = "   <- equal weights (reported)" if w == 0.5 else ""
            print(f"     blend w={w:<4}   {auroc([w*m + (1-w)*p for m, p, _ in data], ys):.3f}{tag}")

    print("\n  6. Training-split calibration (Appendix): net = TP*R - FP*D, R=16.1%, D=76.5%")
    for bud, k, prec in ((0.1, 150, 0.973), (0.2, 300, 0.957), (0.4, 600, 0.907),
                         (0.5, 750, 0.880), (0.7, 1050, 0.821), (1.0, 1500, 0.712)):
        t = round(prec * k)
        print(f"     {bud:4.0%}  flagged {k:5d}  TP {t:5d}  FP {k-t:4d}  net {t*0.161 - (k-t)*0.765:+7.1f}")
    print("=" * 72)


if __name__ == "__main__":
    main()
