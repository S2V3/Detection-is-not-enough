# Stored outputs behind the paper (v1)

These files are copies of finished runs in the [`results` branch of S2V3/fade](https://github.com/S2V3/fade/tree/results). They are what `src/check_paper_numbers.py` reads.

| Folder | Source run in the archive | Contents |
|---|---|---|
| `test/` | `results/store_ctctest_audit2_a1_final_20260903_144740` | the 1,319 GSM8K test questions: first-attempt traces with `p_wrong` and flags (`results.jsonl`), the 988 metamorphic probes (`mpv_probes.jsonl`), per-question correctness of each candidate (`mpv_per_question.jsonl`), the scored report (`mpv_report.json`), run settings (`run_summary.json`, `config_snapshot.json`, `mpv_provenance.json`) |
| `dev/` | `results/store_ctcval_train_audit2_a2_final_20260902_050134` | the 400-question development check: detector AUROC 0.770 and settings |
| `detector/` | `results/ctc2_audit2_latest` | the trained static detector's report (`ctc2_report.json`); the model file `ctc2.joblib` (85 MB) stays in the archive |

Note on the blend: `test/mpv_report.json` records `auroc_blend = 0.778` at `blend_w = 0.25`. That weight was chosen by maximising AUROC on the test set. The paper reports the equal-weight value, 0.773, and the range over weights 0.1 to 0.9 (0.769 to 0.778); `check_paper_numbers.py` recomputes the whole grid.
