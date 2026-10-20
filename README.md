# FADE: Detection Is Not Enough

Code and results for the paper

> **Detection Is Not Enough: Reasoning Traces as Testable Program Hypotheses**
> Vaidehi Hegde, Indian Institute of Technology (Indian School of Mines) Dhanbad
> arXiv: *link to be added*

The paper asks how far a single chain-of-thought trace can be verified with no reference solution, no judge model and no weight update, using a frozen LLaMA-2-7B-chat on GSM8K. It reports three findings:

1. A static detector that checks a trace against itself reaches AUROC 0.741 on the test set, and most failures (67.1%) contain no false equation.
2. A **metamorphic probe** that extracts a program from the trace, executes it on a perturbed question and compares the prediction with the same model's answer exposes many of those failures.
3. No tested retry policy improves accuracy significantly, and an accounting identity shows why: a flag pays only when detector precision exceeds `D / (R + D)`.

Every measurement in the pipeline is made with regular expressions and `sympy`; no language model grades anything.

## Check the paper's numbers (CPU only, about two minutes)

```bash
pip install -r requirements.txt
cd src
python check_paper_numbers.py
```

This recomputes, from the stored test outputs in [`results/paper_v1/`](results/paper_v1/), the probe verdict table, the refutation rate by failure type, the accuracy of every policy with McNemar tests, the repair and damage rates and break-even precision, the detection AUROCs (including the blend over a grid of weights) and the training-split calibration table. [`REPRODUCE.md`](REPRODUCE.md) maps each number in the paper to the script and file it comes from.

## Repository layout

```
Detection-is-not-enough/
├── README.md               this file
├── REPRODUCE.md            paper number -> script -> stored output
├── requirements.txt
├── CITATION.cff
├── src/                    all pipeline code (flat; run every command from src/)
│   ├── artifacts/          fixed seed selection and evaluation order
│   └── check_paper_numbers.py
├── notebooks/              the Kaggle notebooks that ran each stage
└── results/
    ├── paper_v1/           the stored outputs behind the paper's test results
    ├── legacy_exports/     flat exports of earlier runs, kept for history
    └── README.md           index of the full run archive (see below)
```

The modules in `src/` import each other by name, so they are kept in one directory and every script is run from inside `src/`.

## What the main modules do

The code uses project-internal names; the paper uses descriptive ones.

| In the code | In the paper | Main files |
|---|---|---|
| `kaggle_run.py` | the generation pipeline: first attempt, diagnosis, retry | `kaggle_run.py`, `generation.py`, `exemplar_selector.py`, `similarity.py`, `loopguard.py`, `preprocessing.py` |
| extraction and scoring | equation chain and the four trace signals | `extraction.py`, `components.py`, `categorizer.py`, `classification.py` |
| diagnosis | failure taxonomy (WP, SM, CE, ST, AL, NR, TR, UNCLASSIFIED) | `diagnosis.py`, `negatives.py`, `cure_bank.py`, `symbolic_repair.py` |
| CTC (v2) | static detector `p_wrong` and its type head | `ctc.py`, `ctc_data.py`, `ctc_features.py`, `ctc_train2.py`, `run_ctc_validate.py` |
| MPV | metamorphic probe | `mpv.py`, `run_mpv.py`, `score_mpv.py`, `blend_check.py`, `mpv_offline_check.py` |
| selector | gold-free choice between first attempt and retry | `selector.py`, `score_selector.py` |
| statistics | McNemar and Fisher tests, intervals | `stats.py` |

Other groups of scripts belong to work that is not part of the paper's first version: `fst_*`, `features.py`, `run_predictive.py` and `run_stability.py` (predicting the failure type before the first attempt); `run_multicure.py` and `score_multicure.py`; and `nm_*` (re-running the pipeline on Qwen3.5-4B and GSM-Symbolic, in progress).

## Running the full pipeline

The experiments ran on Kaggle (one NVIDIA T4) with `meta-llama/Llama-2-7b-chat-hf`, frozen, `max_new_tokens = 320`, an exemplar budget of 8 and three-stage retrieval from a pool of the model's own correct traces. Each notebook in `notebooks/` clones this repository and runs one stage:

| Stage | Notebook | Entry point |
|---|---|---|
| training run (first attempts, diagnosis, retries) | `fade-typed.ipynb`, `fade-generic.ipynb` | `kaggle_run.py` |
| static detector training | `ctc-train.ipynb` | `ctc_data.py`, `ctc_train2.py` |
| held-out development check | `ctc-validate.ipynb` | `run_ctc_validate.py` |
| test run | `fade_ctc_test.ipynb` | `run_ctc_validate.py` |
| metamorphic probe and scoring | — | `run_mpv.py`, `score_mpv.py`, `blend_check.py` |
| selection policies | `fade_selector.ipynb` | `selector.py`, `score_selector.py` |

The notebooks expect two Kaggle secrets: `HF_TOKEN` (to download the model) and `GH_TOKEN` (to push run outputs to the run archive described below). No token is stored in this repository.

## Run archive

Every run pushed its raw outputs, checkpoint by checkpoint, to the [`results` branch of S2V3/fade](https://github.com/S2V3/fade/tree/results) (62 runs, about 550 MB). This repository holds the code and the outputs behind the paper; [`results/README.md`](results/README.md) indexes the archive. The trained detector (`ctc2.joblib`, 85 MB) is in the archive at `results/ctc2_audit2_latest/`.

## Citation

See [`CITATION.cff`](CITATION.cff).
