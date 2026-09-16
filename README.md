# AFLGopher: Feasibility-Aware Directed Greybox Fuzzing

Source code for AFLGopher, a directed greybox fuzzer that uses a learned feasibility
model to steer the fuzzer toward paths that can actually reach the target site.

**Papers**
- Weiheng Bai, Kefu Wu, Qiushi Wu, Kangjie Lu. *AFLGopher: Accelerating Directed
  Fuzzing via Feasibility-Aware Guidance.* arXiv:2511.10828, November 2025 (extended version).
- Weiheng Bai, Kefu Wu, Qiushi Wu, Kangjie Lu. *Guiding Directed Fuzzing with
  Feasibility.* IEEE European Symposium on Security and Privacy Workshops (EuroS&PW), 2023.
  DOI: 10.1109/EuroSPW59978.2023.00010

## Approach

AFLGopher groups unreached and hard-to-reach basic blocks with reachable ones
(DBSCAN), predicts the feasibility of each outgoing edge with a sequence model (LSTM),
and folds the predicted feasibility into the distance metric that drives seed
scheduling — refining a quantity static analysis already estimates rather than
replacing the analysis.

## Results (extended evaluation, arXiv 2511.10828)

Against four state-of-the-art directed fuzzers (AFLGo, BEACON, WindRanger,
SelectFuzz, AFLGo) and an enhanced version of AFLGo, AFLGopher reaches target sites 2.5–3.8× faster and triggers
known vulnerabilities 4.5–5.6× faster.

## Layout

- `CFG_phase/` — control-flow graph extraction and basic-block grouping
- `Pre-Process/` — data preparation for the feasibility model
- `aflgopher/` — the fuzzer
- `build.sh` — build script
