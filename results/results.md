# DALAN experiment results

Seed evaluation set: 246 queries (216 answerable, 30 out-of-domain); languages: en=82, ceb=69, tl=46, mix=49.
Protocol: 10 x 5-fold stratified CV (50 folds). Mean +/- SD over folds. Reader assumptions rho=0.9, rho_d=0.7. eps=delta=0.05 for DALAN.

## Main results

| Method | Accuracy % | Wrong % | Silent err % | LLM calls % | Skip % | Abstain % | OOD abstain recall % | Latency GPU ms | Latency CPU ms |
|---|---|---|---|---|---|---|---|---|---|
| B0 Always-RAG (LLM for every query) | 77.3 +/- 4.1 | 14.7 +/- 1.0 | 0.0 +/- 0.0 | 100.0 +/- 0.0 | 0.0 +/- 0.0 | 0.0 +/- 0.0 | 0.0 +/- 0.0 | 1500 | 8000 |
| B1 Lexical, fixed thresholds (prototype) | 77.2 +/- 5.5 | 13.0 +/- 3.7 | 13.0 +/- 3.7 | 0.0 +/- 0.0 | 82.1 +/- 4.3 | 17.9 +/- 4.3 | 67.7 +/- 15.0 | 0 | 0 |
| B2 Hybrid lexical+char, fixed thresholds | 78.1 +/- 5.6 | 12.2 +/- 3.7 | 12.2 +/- 3.7 | 0.0 +/- 0.0 | 82.1 +/- 4.3 | 17.9 +/- 4.3 | 67.7 +/- 15.0 | 0 | 0 |
| B3 CSN + hybrid, fixed thresholds | 89.3 +/- 3.2 | 10.7 +/- 3.2 | 10.4 +/- 3.2 | 1.5 +/- 1.7 | 91.2 +/- 2.1 | 7.3 +/- 2.1 | 61.5 +/- 17.2 | 22 | 117 |
| A1 DALAN without CSN | 80.9 +/- 4.8 | 6.6 +/- 2.6 | 4.1 +/- 3.2 | 19.4 +/- 7.4 | 60.5 +/- 7.5 | 20.1 +/- 4.8 | 68.2 +/- 15.7 | 291 | 1551 |
| A2 DALAN without char channel | 88.0 +/- 3.7 | 6.8 +/- 3.3 | 5.0 +/- 3.6 | 12.8 +/- 8.8 | 73.2 +/- 9.2 | 14.0 +/- 3.4 | 78.3 +/- 14.4 | 193 | 1027 |
| A3 DALAN without code-switch features | 89.7 +/- 3.7 | 5.8 +/- 2.9 | 4.5 +/- 3.1 | 9.7 +/- 4.7 | 77.3 +/- 5.8 | 13.0 +/- 4.4 | 71.2 +/- 14.9 | 146 | 775 |
| A4 DALAN with global thresholds | 89.8 +/- 3.9 | 5.7 +/- 3.2 | 5.4 +/- 3.3 | 1.7 +/- 2.0 | 83.9 +/- 4.6 | 14.4 +/- 4.3 | 81.6 +/- 14.7 | 26 | 137 |
| DALAN (full) | 91.8 +/- 3.0 | 5.3 +/- 2.6 | 4.2 +/- 2.8 | 7.5 +/- 4.5 | 80.2 +/- 4.9 | 12.2 +/- 3.5 | 77.1 +/- 15.4 | 114 | 603 |

Latency = measured routing time + LLM call rate x assumed generation time (1500 ms GPU 7B 4-bit, 8000 ms CPU 3B 4-bit).
Mean routing time for DALAN: 0.57 ms per query (Python, single core).

## Accuracy by language (DALAN vs baselines)

| Method | en acc % | ceb acc % | tl acc % | mix acc % | en wrong % | ceb wrong % | tl wrong % | mix wrong % |
|---|---|---|---|---|---|---|---|---|
| B1 Lexical, fixed thresholds (prototype) | 82.9 | 65.2 | 65.1 | 96.0 | 17.1 | 15.9 | 10.9 | 4.0 |
| B2 Hybrid lexical+char, fixed thresholds | 82.9 | 65.2 | 67.3 | 98.0 | 17.1 | 15.9 | 8.7 | 2.0 |
| B3 CSN + hybrid, fixed thresholds | 82.9 | 89.8 | 94.3 | 94.8 | 17.1 | 10.2 | 5.7 | 5.2 |
| A1 DALAN without CSN | 88.6 | 69.4 | 69.1 | 95.3 | 9.6 | 7.5 | 4.3 | 2.6 |
| DALAN (full) | 87.9 | 90.1 | 95.4 | 97.1 | 7.0 | 8.4 | 2.2 | 1.0 |

## Oracle reader (rho = rho_d = 1)

| Method | Accuracy % | Wrong % | LLM calls % |
|---|---|---|---|
| B0 Always-RAG (LLM for every query) | 88.6 | 0.0 | 100.0 |
| B1 Lexical, fixed thresholds (prototype) | 77.2 | 13.0 | 0.0 |
| B2 Hybrid lexical+char, fixed thresholds | 78.1 | 12.2 | 0.0 |
| B3 CSN + hybrid, fixed thresholds | 89.6 | 10.4 | 1.5 |
| A1 DALAN without CSN | 83.3 | 4.1 | 19.4 |
| A2 DALAN without char channel | 89.6 | 5.0 | 12.8 |
| A3 DALAN without code-switch features | 91.1 | 4.5 | 9.7 |
| A4 DALAN with global thresholds | 90.0 | 5.4 | 1.7 |
| DALAN (full) | 92.9 | 4.2 | 7.5 |

## Paired Wilcoxon signed-rank tests vs DALAN (full), p-values over folds

| Compared with | Accuracy | Wrong-answer rate | LLM call rate |
|---|---|---|---|
| B0 Always-RAG (LLM for every query) | 7.6e-10 | 1.8e-15 | 7.5e-10 |
| B1 Lexical, fixed thresholds (prototype) | 1.8e-15 | 7.6e-10 | 1.1e-09 |
| B2 Hybrid lexical+char, fixed thresholds | 1.8e-15 | 8e-10 | 1.1e-09 |
| B3 CSN + hybrid, fixed thresholds | 7.3e-07 | 8e-10 | 1.2e-08 |
| A1 DALAN without CSN | 1.8e-15 | 0.0011 | 1.2e-09 |
| A2 DALAN without char channel | 2e-08 | 0.00023 | 1.2e-05 |
| A3 DALAN without code-switch features | 1.4e-05 | 0.019 | 0.0076 |
| A4 DALAN with global thresholds | 6.2e-07 | 0.41 | 1.5e-08 |

Folds from repeated CV are not independent, so treat these p-values as indicative; confirm on a held-out real-query test set.

## Calibration quality (pooled out-of-fold predictions, first repeat)

| Calibrator | ECE all | Brier all | ECE code-switched | ECE English |
|---|---|---|---|---|
| DALAN (full) | 0.049 | 0.062 | 0.045 | 0.097 |
| A3 without code-switch features | 0.037 | 0.082 | 0.027 | 0.090 |

## Operating points (Pareto sweep, see pareto.png / pareto.csv)

| Method | param | LLM calls % | Wrong % | Accuracy % |
|---|---|---|---|---|
| DALAN (eps sweep) | 0.0 | 28.2 | 4.2 | 90.5 |
| DALAN (eps sweep) | 0.01 | 24.1 | 4.2 | 90.5 |
| DALAN (eps sweep) | 0.02 | 21.7 | 4.8 | 90.0 |
| DALAN (eps sweep) | 0.03 | 16.5 | 5.3 | 90.1 |
| DALAN (eps sweep) | 0.05 | 8.0 | 5.3 | 92.1 |
| DALAN (eps sweep) | 0.08 | 3.3 | 8.3 | 90.1 |
| DALAN (eps sweep) | 0.1 | 2.2 | 10.2 | 88.2 |
| DALAN (eps sweep) | 0.15 | 0.0 | 13.9 | 85.0 |
| DALAN (eps sweep) | 0.2 | 0.0 | 15.8 | 84.2 |
| DALAN (eps sweep) | 0.3 | 0.0 | 17.7 | 82.3 |
| B2 hybrid (threshold sweep) | 3 | 0.0 | 12.1 | 78.2 |
| B2 hybrid (threshold sweep) | 4 | 0.0 | 12.1 | 78.2 |
| B2 hybrid (threshold sweep) | 5 | 0.0 | 12.1 | 78.2 |
| B2 hybrid (threshold sweep) | 6 | 0.0 | 12.1 | 78.2 |
| B2 hybrid (threshold sweep) | 8 | 0.0 | 12.1 | 78.2 |
| B2 hybrid (threshold sweep) | 10 | 8.1 | 9.1 | 80.9 |
| B2 hybrid (threshold sweep) | 12 | 13.0 | 8.1 | 81.9 |
| B2 hybrid (threshold sweep) | 15 | 14.6 | 7.9 | 82.1 |
| B2 hybrid (threshold sweep) | 20 | 14.6 | 7.9 | 82.1 |
| B3 CSN + hybrid (threshold sweep) | 3 | 0.0 | 10.9 | 89.1 |
| B3 CSN + hybrid (threshold sweep) | 4 | 0.4 | 10.6 | 89.4 |
| B3 CSN + hybrid (threshold sweep) | 5 | 1.4 | 10.7 | 89.3 |
| B3 CSN + hybrid (threshold sweep) | 6 | 1.4 | 10.7 | 89.3 |
| B3 CSN + hybrid (threshold sweep) | 8 | 1.6 | 10.8 | 89.2 |
| B3 CSN + hybrid (threshold sweep) | 10 | 6.1 | 10.1 | 89.9 |
| B3 CSN + hybrid (threshold sweep) | 12 | 11.5 | 9.0 | 91.0 |
| B3 CSN + hybrid (threshold sweep) | 15 | 14.2 | 8.6 | 91.4 |
| B3 CSN + hybrid (threshold sweep) | 20 | 14.9 | 8.3 | 91.7 |

Gloss weight gamma chosen on training folds: 0.4: 40 folds, 0.6: 10 folds.
