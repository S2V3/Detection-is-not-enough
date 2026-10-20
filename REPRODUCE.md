# Reproducing the paper's numbers

All test-set numbers below are recomputed by `src/check_paper_numbers.py` from the stored outputs in `results/paper_v1/test/`, which is a copy of the run `store_ctctest_audit2_a1_final_20260903_144740` on the `results` branch. Correctness labels come from `mpv_per_question.jsonl`, written by `score_mpv.py` after the reference answers were opened once, at the end of the run.

| Paper result | Value | Recomputed from |
|---|---|---|
| Static detector AUROC, test | 0.741 | `results.jsonl` (`p_wrong`) + `mpv_per_question.jsonl` |
| Static detector AUROC, development (400) | 0.770 | `paper_v1/dev/run_summary.json` (`auroc`) |
| Flags at the 40% cut (`p_wrong >= 0.683`) | 540 (40.9%), precision 87.6% | `results.jsonl` (`flagged`) |
| Repair rate R, damage rate D | 58/473 = 12.3%, 50/67 = 74.6% | `mpv_per_question.jsonl` (`pass1`, `retry`) |
| Break-even precision, net change | 85.9%, +8 | as above |
| Probe coverage | 988 probes over 937 of 1,319 questions; 847 with a parseable first answer | `mpv_probes.jsonl`, `mpv_report.json` (`detection.n`) |
| Questions decided by probe evidence | 90 | `mpv_report.json` (`reasons`: metamorphic 68 + program 22) |
| Probe verdicts | supported 241 (146 correct, 60.6%); refuted 606 (122 correct); base rate 31.6%; odds ratio 6.1; Fisher p = 5.6e-29 | `mpv_report.json` (`support_precision`) |
| Refutation by failure type | e.g. WP 140/180, SM 157/185, correct traces 122/268 | `mpv_report.json` (`refuted_by_type`) |
| Accuracy of every policy | pass-1 367 (27.82%) ... select (metamorphic) 382 (28.96%), McNemar p = 0.091 | `mpv_report.json` |
| Detection AUROC on the 847 testable traces | p_wrong 0.740, probe 0.698, equal-weight blend 0.773 (0.769–0.778 over weights 0.1–0.9) | `results.jsonl` + `mpv_probes.jsonl`, re-executed with `mpv.py` |
| Training-split calibration table | 10% +20.4 ... 40% +44.7 ... 100% −158.5 | rows recorded in `run_ctc_validate.py` (audit D67), recomputed as TP·R − FP·D with R = 16.1%, D = 76.5% |

Numbers that come from the training run (failure taxonomy, repair rates on the 1,068 training failures, out-of-fold detector estimates) are produced by `kaggle_run.py`, `diagnosis.py` and `ctc_train2.py` from the training stores on the `results` branch; see `results/README.md`.
