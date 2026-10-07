print("Running OUTC script")

import matplotlib
matplotlib.use("Agg")

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

REQUIRED = ["DEMO25Q4.txt", "REAC25Q4.txt", "OUTC25Q4.txt"]
missing = [name for name in REQUIRED if not Path(name).is_file()]
if missing:
    raise SystemExit(
        "Missing FAERS files: " + ", ".join(missing) + ". "
        "Download the Q4 2025 ASCII files from "
        "https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html "
        "and place them in this directory."
    )

# Death, life-threatening, hospitalisation, disability, congenital anomaly,
# required intervention. Matches the project definition of a serious case.
SERIOUS_CODES = {"DE", "LT", "HO", "DS", "CA", "RI"}


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
    demo = demo.sort_values("caseversion", ascending=False, na_position="last")
    return demo.drop_duplicates("caseid")


def take_sample(ids, n, label):
    if ids.empty:
        raise SystemExit(f"No {label} cases after cleaning.")
    n_take = min(n, len(ids))
    if n_take < n:
        print(f"Only {len(ids)} {label} cases; sampling {n_take}.")
    return ids.sample(n_take, random_state=42)


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

reac = load_faers("REAC25Q4.txt")[["primaryid", "pt"]].copy()
reac["primaryid"] = as_id(reac["primaryid"])
reac = reac[reac["primaryid"].isin(valid_ids)]
reac["pt"] = reac["pt"].astype("string").str.strip()
reac = reac.dropna(subset=["pt"])
reac = reac[reac["pt"] != ""]
reac = reac.drop_duplicates(["primaryid", "pt"])

outc = load_faers("OUTC25Q4.txt")[["primaryid", "outc_cod"]].copy()
outc["primaryid"] = as_id(outc["primaryid"])
outc = outc[outc["primaryid"].isin(valid_ids)]
outc["outc_cod"] = outc["outc_cod"].astype("string").str.strip().str.upper()

serious_ids = outc.loc[outc["outc_cod"].isin(SERIOUS_CODES), "primaryid"].drop_duplicates()
serious_id_set = set(serious_ids)
non_serious_ids = demo.loc[~demo["primaryid"].isin(serious_id_set), "primaryid"].drop_duplicates()
print(f"Serious IDs: {len(serious_ids)}, Non-serious IDs: {len(non_serious_ids)}")

sample_serious = take_sample(serious_ids, 5000, "serious")
sample_non_serious = take_sample(non_serious_ids, 5000, "non-serious")
sample_ids = set(sample_serious).union(set(sample_non_serious))

reac_s = reac[reac["primaryid"].isin(sample_ids)].copy()
if reac_s.empty:
    raise SystemExit("Sampled cases have no reactions.")
reac_s["is_serious"] = reac_s["primaryid"].isin(serious_id_set)

serious_df = reac_s[reac_s["is_serious"]]
non_serious_df = reac_s[~reac_s["is_serious"]]
print(f"Serious rows: {len(serious_df)}, Non-serious rows: {len(non_serious_df)}")

overall_pct = reac_s["pt"].value_counts(normalize=True)
serious_pct = serious_df["pt"].value_counts(normalize=True)
non_serious_pct = non_serious_df["pt"].value_counts(normalize=True)

# Keep each group's top 10, but look up the real share in every column.
# Taking head(10) before concatenating left the other columns blank.
top_pts = list(overall_pct.head(10).index)
for pt in list(serious_pct.head(10).index) + list(non_serious_pct.head(10).index):
    if pt not in top_pts:
        top_pts.append(pt)

comparison = pd.DataFrame({
    "Overall": overall_pct.reindex(top_pts),
    "Serious": serious_pct.reindex(top_pts),
    "Non-serious": non_serious_pct.reindex(top_pts),
}).fillna(0.0)
comparison.index.name = "pt"
print(comparison)
comparison.to_csv("reaction_comparison_table.csv")

save_bar(overall_pct.head(10), "Overall Reaction Distribution (Subset)", "overall_subset_reactions.png")
save_bar(serious_pct.head(10), "Serious Reaction Distribution", "serious_subset_reactions.png")
save_bar(non_serious_pct.head(10), "Non-Serious Reaction Distribution", "non_serious_subset_reactions.png")
