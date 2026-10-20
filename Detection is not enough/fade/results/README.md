# Run archive (`results` branch)

Every run pushes its outputs to the `results` branch of this repository as a folder named `store_<run>_<status>_<timestamp>`. A run writes an `inprogress` folder while it runs and a `final_<timestamp>` folder when it finishes; when several `final` folders exist for one run, the latest is the complete one. The notebooks restore interrupted runs from this layout, so the branch is left as it is.

The run used for the paper's test results is `store_ctctest_audit2_a1_final_20260903_144740`; a copy is in [`paper_v1/test/`](paper_v1/test/).

## Training runs (first attempts, diagnosis, retries)

| Folder | Status |
|---|---|
| `store_deferredonly_train_audit2_final_20260831_044850` | final |
| `store_deferredonly_train_audit2_inprogress` | in progress (superseded) |
| `store_generic_train_audit2_d40_inprogress` | in progress (superseded) |
| `store_generic_train_audit2_final_20260831_091111` | final |
| `store_generic_train_audit2_final_20260831_151605` | final |
| `store_generic_train_audit2_inprogress` | in progress (superseded) |
| `store_typed_train_audit2_d40_inprogress` | in progress (superseded) |
| `store_typed_train_audit2_d53_final_20260901_065724` | final |
| `store_typed_train_audit2_d53_inprogress` | in progress (superseded) |
| `store_typed_train_audit2_d57_final_20260901_105931` | final |
| `store_typed_train_audit2_d57_final_20260901_144401` | final |
| `store_typed_train_audit2_d57_inprogress` | in progress (superseded) |
| `store_typed_train_audit2_d61_inprogress` | in progress (superseded) |
| `store_typed_train_audit2_d63_final_20260901_235308` | final |
| `store_typed_train_audit2_d63_inprogress` | in progress (superseded) |
| `store_typed_train_audit2_final_20260829_175520` | final |
| `store_typed_train_audit2_final_20260830_030613` | final |
| `store_typed_train_audit2_inprogress` | in progress (superseded) |
| `store_typed_train_final_20260828_220401` | final |
| `store_typed_train_inprogress` | in progress (superseded) |

## Trained static detector (CTC v2)

| Folder | Status |
|---|---|
| `ctc2_audit2_20260902_015035` | — |
| `ctc2_audit2_latest` | — |

## Development checks (400 held-out training questions)

| Folder | Status |
|---|---|
| `store_ctcabl_generic_audit2_a1_final_20260902_172544` | final |
| `store_ctcabl_generic_audit2_a1_inprogress` | in progress (superseded) |
| `store_ctcval_train_audit2_a2_final_20260902_050134` | final |
| `store_ctcval_train_audit2_a2_inprogress` | in progress (superseded) |
| `store_ctcval_train_audit2_final_20260831_133053` | final |
| `store_ctcval_train_audit2_final_20260902_020013` | final |
| `store_ctcval_train_audit2_inprogress` | in progress (superseded) |

## Test set (1,319 questions): detector, retries and metamorphic probes

| Folder | Status |
|---|---|
| `store_ctctest_audit2_a1_final_20260902_145411` | final |
| `store_ctctest_audit2_a1_final_20260903_080034` | final |
| `store_ctctest_audit2_a1_final_20260903_144334` | final |
| `store_ctctest_audit2_a1_final_20260903_144740` | final **(paper v1 test results)** |
| `store_ctctest_audit2_a1_inprogress` | in progress (superseded) |

## Inline immediate-retry baseline

| Folder | Status |
|---|---|
| `store_immediate_20260727_090828` | — |

## Failure-type stability study (not in paper v1)

| Folder | Status |
|---|---|
| `stability_final_20260808_231730` | final |
| `stability_final_20260808_231759` | final |
| `stability_inprogress` | in progress (superseded) |

## New model and second dataset (Qwen3.5-4B, GSM-Symbolic), in progress, not in paper v1

| Folder | Status |
|---|---|
| `store_nm_llama2_test_gsm8k_final_20260927_221628` | final |
| `store_nm_llama2_test_gsm8k_inprogress` | in progress (superseded) |
| `store_nm_llama2_test_p1_final_20260928_001744` | final |
| `store_nm_llama2_test_p1_inprogress` | in progress (superseded) |
| `store_nm_qwen35_4b_train_s0_final_20260926_184306` | final |
| `store_nm_qwen35_4b_train_s0_inprogress` | in progress (superseded) |
| `store_nm_qwen35_4b_train_s1_final_20260926_184310` | final |
| `store_nm_qwen35_4b_train_s1_inprogress` | in progress (superseded) |
| `store_nm_qwen35_4b_v2_ctc_final_20260927_165413` | final |
| `store_nm_qwen35_4b_v2_ctc_inprogress` | in progress (superseded) |
| `store_nm_qwen35_4b_v2_heldout_final_20260927_223746` | final |
| `store_nm_qwen35_4b_v2_heldout_inprogress` | in progress (superseded) |
| `store_nm_qwen35_4b_v2_test_p1_s0_final_20260928_001814` | final |
| `store_nm_qwen35_4b_v2_test_p1_s0_inprogress` | in progress (superseded) |
| `store_nm_qwen35_4b_v2_test_p1_s1_final_20260928_001816` | final |
| `store_nm_qwen35_4b_v2_test_p1_s1_inprogress` | in progress (superseded) |
| `store_nm_qwen35_4b_v2_train_final_20260927_165410` | final |
| `store_nm_qwen35_4b_v2_train_inprogress` | in progress (superseded) |
| `store_nm_qwen35_4b_v2_train_s0_final_20260927_162414` | final |
| `store_nm_qwen35_4b_v2_train_s0_final_20260927_164509` | final |
| `store_nm_qwen35_4b_v2_train_s0_inprogress` | in progress (superseded) |
| `store_nm_qwen35_4b_v2_train_s1_final_20260927_162412` | final |
| `store_nm_qwen35_4b_v2_train_s1_final_20260927_165229` | final |
| `store_nm_qwen35_4b_v2_train_s1_inprogress` | in progress (superseded) |
