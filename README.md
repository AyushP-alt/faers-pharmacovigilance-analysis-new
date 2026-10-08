# FDA FAERS Q4 2025

Dupixent is named in 36,464 cases. Off-label use is reported in 26,853 cases. Death is reported in 13,241 cases.

This repository counts FDA Adverse Event Reporting System (FAERS) reports for the fourth quarter of 2025. The extract has 385,288 cases, and each case is kept once. A drug is counted once per case. A reaction is counted once per case. The charts in `result/` are those counts.

## Drugs

`faers_analysis.py` reads `DEMO25Q4.txt` and `DRUG25Q4.txt`. It keeps the latest `caseversion` for each `caseid`, joins drugs on `primaryid`, and counts distinct `(primaryid, drugname)` pairs. The number on a bar is the number of cases that name the drug.

That number is not a measure of causation. FAERS has a role code for each drug row. `PS` is the primary suspect. `SS` is a secondary suspect. `C` is concomitant. `I` is an interacting drug. Dupixent, Zepbound, Bimzelx, Mounjaro, and Skyrizi are the primary suspect in most of the cases that name them. Prednisone, acetaminophen, aspirin, atorvastatin, and methotrexate usually are not. Aspirin is the primary suspect in 90 of the 9,408 cases that name it.

| Rank | Drug | Cases | Primary suspect in most cases |
| --- | --- | ---: | --- |
| 1 | Dupixent | 36,464 | Yes |
| 2 | Prednisone | 13,023 | No |
| 3 | Acetaminophen | 10,512 | No |
| 4 | Zepbound | 9,666 | Yes |
| 5 | Aspirin | 9,408 | No |
| 6 | Bimzelx | 8,400 | Yes |
| 7 | Mounjaro | 7,950 | Yes |
| 8 | Atorvastatin | 7,156 | No |
| 9 | Methotrexate | 6,718 | No |
| 10 | Skyrizi | 6,295 | Yes |

![Top drugs, one count per case](result/TDR_corrected.png)

## Reactions

The same script reads `REAC25Q4.txt` and counts distinct `(primaryid, pt)` pairs. `pt` is the MedDRA preferred term. The number on a bar is the number of cases that report the term.

| Rank | Reaction | Cases |
| --- | --- | ---: |
| 1 | Off label use | 26,853 |
| 2 | Drug ineffective | 22,270 |
| 3 | Product dose omission issue | 17,356 |
| 4 | Fatigue | 15,718 |
| 5 | Diarrhoea | 14,774 |
| 6 | Nausea | 14,759 |
| 7 | Death | 13,241 |
| 8 | Headache | 11,965 |
| 9 | Pruritus | 11,461 |
| 10 | Dyspnoea | 10,701 |

![Top reactions, one count per case](result/ADR_corrected.png)

## Serious and non-serious cases

`faers_outc_analysis.py` reads `OUTC25Q4.txt`. A case is serious when its latest report has any of these outcome codes:

| Code | Outcome |
| --- | --- |
| DE | Death |
| LT | Life-threatening |
| HO | Hospitalisation |
| DS | Disability |
| CA | Congenital anomaly |
| RI | Required intervention |

The full file has 108,869 serious cases and 276,419 other cases. Another 109,473 cases carry only `OT` (other medically important) and are left in the non-serious group.

The script draws 5,000 serious cases and 5,000 non-serious cases with `random_state=42`. Within each group it counts each reaction once per case, then divides by the number of reaction rows in that group. A bar is a share of reaction terms, not a share of cases. Death is recorded in 13,037 of the 108,869 serious cases. In the serious sample it is 2.47% of reaction terms, because most cases list more than one term.

The sample is balanced. The file is not, so the overall bars are not the rate across all 385,288 cases.

- Serious terms: Death 2.47%, off-label use 1.53%, diarrhoea 1.03%.
- Non-serious terms: off-label use 2.34%, drug ineffective 1.95%, product dose omission 1.72%.
- Pooled sample: off-label use 1.84%, Death 1.53%.

![Overall sample](result/overall_subset_reactions_corrected.png)

![Serious sample](result/serious_subset_reactions_corrected.png)

![Non-serious sample](result/non_serious_subset_reactions_corrected.png)

## Scripts and data

- `faers_analysis.py` writes the full-file drug and reaction charts.
- `faers_outc_analysis.py` writes the serious and non-serious charts.

The Q4 2025 ASCII files are not in this repository. They come from the FDA FAERS public dashboard: https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html

Requirements: pandas, matplotlib.

Earlier charts are in `archive/`. The note on how those counts differ from the charts above is `change.pdf`.
