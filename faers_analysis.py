import matplotlib
matplotlib.use("Agg")

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

REQUIRED = ["DEMO25Q4.txt", "DRUG25Q4.txt", "REAC25Q4.txt"]
missing = [name for name in REQUIRED if not Path(name).is_file()]
if missing:
    raise SystemExit(
        "Missing FAERS files: " + ", ".join(missing) + ". "
        "Download the Q4 2025 ASCII files from "
        "https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html "
        "and place them in this directory."
    )


def load_faers(path):
    df = pd.read_csv(path, sep="$", encoding="latin1", low_memory=False)
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
    # Highest numeric caseversion is the latest follow-up. String sort would
    # keep version 9 ahead of version 10.
    demo = demo.sort_values("caseversion", ascending=False, na_position="last")
    return demo.drop_duplicates("caseid")


def save_bar(series, title, path):
    fig, ax = plt.subplots(figsize=(10, 6))
    series.plot(kind="bar", ax=ax, title=title)
    ax.tick_params(axis="x", labelrotation=45)
    for label in ax.get_xticklabels():
        label.set_ha("right")
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


demo = latest_cases(load_faers("DEMO25Q4.txt"))
valid_ids = set(demo["primaryid"])

drug = load_faers("DRUG25Q4.txt")[["primaryid", "drugname"]].copy()
drug["primaryid"] = as_id(drug["primaryid"])
drug = drug[drug["primaryid"].isin(valid_ids)]
drug["drugname"] = drug["drugname"].astype("string").str.upper().str.strip()
drug = drug.dropna(subset=["drugname"])
drug = drug[drug["drugname"] != ""]
# One drug can be listed several times on a case (dose, route). Count the case once.
drug = drug.drop_duplicates(["primaryid", "drugname"])

reac = load_faers("REAC25Q4.txt")[["primaryid", "pt"]].copy()
reac["primaryid"] = as_id(reac["primaryid"])
reac = reac[reac["primaryid"].isin(valid_ids)]
reac["pt"] = reac["pt"].astype("string").str.strip()
reac = reac.dropna(subset=["pt"])
reac = reac[reac["pt"] != ""]
reac = reac.drop_duplicates(["primaryid", "pt"])

print(f"Latest cases: {len(demo)}")
print(f"Drug rows: {len(drug)}")
print(drug.head())
print(f"Reaction rows: {len(reac)}")
print(reac.head())

top_reactions = reac["pt"].value_counts().head(10)
top_drugs = drug["drugname"].value_counts().head(10)
print(top_reactions)
print(top_drugs)

save_bar(top_reactions, "Top Adverse Reactions", "top_reactions.png")
save_bar(top_drugs, "Top Drugs Reported", "top_drugs.png")
