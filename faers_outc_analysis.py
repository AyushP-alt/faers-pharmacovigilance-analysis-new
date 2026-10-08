print("Running OUTC script")

import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULT = ROOT / "result"
RESULT.mkdir(exist_ok=True)

REQUIRED = ["DEMO25Q4.txt", "REAC25Q4.txt", "OUTC25Q4.txt"]
missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
if missing:
    raise SystemExit(
        "Missing FAERS files: " + ", ".join(missing) + ". "
        "Download the Q4 2025 ASCII files from "
        "https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html "
        "and place them in this directory."
    )

# Death, life-threatening, hospitalisation, disability, congenital anomaly,
# required intervention, and other medically important. OT is serious.
SERIOUS_CODES = {"DE", "LT", "HO", "DS", "CA", "RI", "OT"}


def load_faers(name, columns):
    df = pd.read_csv(
        ROOT / name,
        sep="$",
        encoding="latin1",
        low_memory=False,
        usecols=lambda col: col.strip().lower() in columns,
    )
    df.columns = df.columns.str.strip().str.lower()
    return df


def as_id(series):
    numeric = pd.to_numeric(series, errors="coerce")
    if series.notna().sum() == numeric.notna().sum():
        return numeric.astype("Int64").astype("string")
    return series.astype("string").str.strip()


def latest_cases(demo):
    demo = demo.copy()
    demo["primaryid"] = as_id(demo["primaryid"])
    demo["caseid"] = as_id(demo["caseid"])
    demo["caseversion"] = pd.to_numeric(demo["caseversion"], errors="coerce")
    demo = demo.dropna(subset=["primaryid", "caseid"])
    demo = demo.sort_values("caseversion", ascending=False, na_position="last")
    return demo.drop_duplicates("caseid")


demo = latest_cases(load_faers("DEMO25Q4.txt", {"primaryid", "caseid", "caseversion"}))
valid_ids = set(demo["primaryid"])

outc = load_faers("OUTC25Q4.txt", {"primaryid", "outc_cod"})
outc["primaryid"] = as_id(outc["primaryid"])
outc = outc[outc["primaryid"].isin(valid_ids)]
outc["outc_cod"] = outc["outc_cod"].astype("string").str.strip().str.upper()

serious_ids = outc.loc[outc["outc_cod"].isin(SERIOUS_CODES), "primaryid"].drop_duplicates()
serious_id_set = set(serious_ids)
is_serious = demo["primaryid"].isin(serious_id_set)

serious_cases = int(is_serious.sum())
total_cases = int(len(demo))
non_serious_cases = total_cases - serious_cases

counts = pd.DataFrame(
    [
        {
            "serious_cases": serious_cases,
            "non_serious_cases": non_serious_cases,
            "total_cases": total_cases,
        }
    ]
)
counts_path = RESULT / "seriousness_counts.csv"
counts.to_csv(counts_path, index=False)
print(
    f"Step 1: OT is serious and every latest case is counted. "
    f"serious_cases={serious_cases}, non_serious_cases={non_serious_cases}, "
    f"total_cases={total_cases}"
)

reac = load_faers("REAC25Q4.txt", {"primaryid", "pt"})
reac["primaryid"] = as_id(reac["primaryid"])
reac = reac[reac["primaryid"].isin(valid_ids)]
reac["pt"] = reac["pt"].astype("string").str.strip()
reac = reac.dropna(subset=["pt"])
reac = reac[reac["pt"] != ""]
reac = reac.drop_duplicates(["primaryid", "pt"])
reac["is_serious"] = reac["primaryid"].isin(serious_id_set)

reaction = (
    reac.groupby("pt", as_index=False)
    .agg(
        serious_cases=("is_serious", "sum"),
        non_serious_cases=("is_serious", lambda flag: int((~flag).sum())),
    )
)
reaction["serious_cases"] = reaction["serious_cases"].astype(int)
reaction["non_serious_cases"] = reaction["non_serious_cases"].astype(int)
reaction = reaction.sort_values(
    ["serious_cases", "pt"], ascending=[False, True], kind="mergesort"
).head(15)
reaction = reaction[["pt", "serious_cases", "non_serious_cases"]]

reaction_path = RESULT / "reaction_by_seriousness.csv"
reaction.to_csv(reaction_path, index=False)
top_pt = reaction.iloc[0]
print(
    f"Step 2: top 15 preferred terms by serious case count, one term per case. "
    f"{top_pt['pt']} serious_cases={int(top_pt['serious_cases'])}"
)
