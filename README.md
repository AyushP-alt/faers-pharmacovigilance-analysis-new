# FDA FAERS Q4 2025

Dupixent is named in 36,464 cases. Off-label use is reported in 26,853 cases. Death is reported in 13,241 cases. Of the 385,288 cases, 218,342 are serious.

This repository counts FDA Adverse Event Reporting System (FAERS) reports for the fourth quarter of 2025. The extract has 385,288 cases, and each case is kept once. A drug is counted once per case. A reaction is counted once per case. The charts in `result/` for drugs and reactions are those counts.

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

`faers_outc_analysis.py` reads `OUTC25Q4.txt` and keeps the latest `caseversion` for each `caseid`. A case is serious when that version has any of these outcome codes. `OT` is other medically important, and it is serious.

| Code | Outcome |
| --- | --- |
| DE | Death |
| LT | Life-threatening |
| HO | Hospitalisation |
| DS | Disability |
| CA | Congenital anomaly |
| RI | Required intervention |
| OT | Other medically important |

A case with none of these codes is non-serious. The script does not draw a sample. `result/seriousness_counts.csv` is the full file.

| Serious cases | Non-serious cases | Total cases |
| ---: | ---: | ---: |
| 218,342 | 166,946 | 385,288 |

On that same file, each preferred term is counted once per case. `result/reaction_by_seriousness.csv` keeps the top 15 terms by serious case count. A row is a case count. It is not a share of a 5,000-case sample, and it is not a rate per 385,288 cases.

| Preferred term | Serious cases | Non-serious cases |
| --- | ---: | ---: |
| Off label use | 17,423 | 9,430 |
| Death | 13,044 | 197 |
| Fatigue | 10,364 | 5,354 |
| Drug ineffective | 10,307 | 11,963 |
| Diarrhoea | 10,064 | 4,710 |
| Nausea | 9,439 | 5,320 |
| Dyspnoea | 7,521 | 3,180 |
| Vomiting | 7,399 | 2,415 |
| Pneumonia | 7,307 | 78 |
| Headache | 7,147 | 4,818 |
| Pain | 6,915 | 3,508 |
| Arthralgia | 6,121 | 3,896 |
| Condition aggravated | 6,039 | 3,940 |
| Pyrexia | 6,018 | 1,001 |
| Malaise | 5,926 | 1,821 |

The two columns add up to the full-file term count. Off-label use is 17,423 + 9,430 = 26,853 cases. The preferred term Death is 13,044 + 197 = 13,241 cases.

## Case notes

`cases/` holds 10 latest-version reports. Every drug row on these cases is `DUPIXENT` or `BIMZELX`. Bimzelx is the second drug because it is the primary suspect on 9,156 of its 9,241 rows. Each note lists only fields present in the extract. An empty field is written as "not reported." Dose, dates, history, and labs are not added.

Four of the ten notes are serious. Primary id 236442575 carries outcome code `DE`.

| PRIMARYID | Drug | Serious | File |
| --- | --- | --- | --- |
| 236442575 | DUPIXENT | yes | [cases/236442575.md](cases/236442575.md) |
| 255529252 | DUPIXENT | yes | [cases/255529252.md](cases/255529252.md) |
| 196559993 | DUPIXENT | yes | [cases/196559993.md](cases/196559993.md) |
| 168525962 | DUPIXENT | no | [cases/168525962.md](cases/168525962.md) |
| 258979652 | BIMZELX | no | [cases/258979652.md](cases/258979652.md) |
| 209157233 | DUPIXENT; BIMZELX | no | [cases/209157233.md](cases/209157233.md) |
| 174912276 | DUPIXENT | no | [cases/174912276.md](cases/174912276.md) |
| 246757656 | BIMZELX | no | [cases/246757656.md](cases/246757656.md) |
| 251272263 | BIMZELX | yes | [cases/251272263.md](cases/251272263.md) |
| 244623883 | BIMZELX; DUPIXENT | no | [cases/244623883.md](cases/244623883.md) |

The index is `cases/case_log.csv`.

## Scripts and data

- `faers_analysis.py` writes the full-file drug and reaction charts.
- `faers_outc_analysis.py` writes `result/seriousness_counts.csv` and `result/reaction_by_seriousness.csv`.

The Q4 2025 ASCII files are not in this repository. They come from the FDA FAERS public dashboard: https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html

Requirements: pandas, matplotlib.

Earlier charts are in `archive/`. The note on how those pair counts differ from the case counts above is `change.pdf`. The subset images in `result/` come from an earlier balanced sample. They are not rates for all 385,288 cases.
