"""
Shadow Docket — Cross-Docket Issue Area Comparison (2020 Term)
Kastellec & Taboni (2026) - shadow_docket_database_v2-0.xlsx
SCDB (2025) - SCDB_2025_01_caseCentered_Citation.csv
Salience data (2020 Term) - issuesalience.xlsx

Spaeth issueArea codes:
  1  Criminal Procedure   (issues 10010-10600)
  2  Civil Rights         (issues 20010-20410)
  3  First Amendment      (issues 30010-30200)
  4  Due Process          (issues 40010-40070)
  5  Privacy              (issues 50010-50040)
  6  Attorneys            (issues 60010-60040)
  7  Unions               (issues 70010-70210)
  8  Economic Activity    (issues 80010-80350)
  9  Judicial Power       (issues 90010-90520)
  10 Federalism           (issues 100010-100130)
  11 Interstate Relations (issues 110010-110030)
  12 Federal Taxation     (issues 120010-120040)
  13 Miscellaneous        (issues 130010-130020)
  14 Private Action       (issues 140010-140080)

Keywords derived from Spaeth issue-level descriptions at:
  http://scdb.wustl.edu/documentation.php?var=issue

High-salience issue areas defined by combining:
  (A) Empirical: mean article coverage above merits median (36 articles)
      Criminal Procedure (111.6), First Amendment (83.7), Civil Rights (65.3)
  (B) Theoretical: sustained presence in shadow docket literature
      Privacy (Shaw 2025), First Amendment + Civil Rights (Smith 2021)

Research Question:
  Do high-salience issue areas appear disproportionately on the shadow
  docket relative to the merits docket in the 2020 Term?

Run: python categorize_shadow_docket.py
"""

import pandas as pd

shadowdocketdata = "data/shadow_docket_database_v2-0.csv"
scdbdata         = "data/SCDB_2025_01_caseCentered_Citation.csv"
saliencedata     = "data/issuesalience.xlsx"

# High-salience issue areas (theory + data combined criterion)
highsalienceareas = ["Criminal Procedure", "First Amendment", "Civil Rights", "Privacy"]

# Spaeth issue area labels
issuearealabels = {
    1:  "Criminal Procedure",
    2:  "Civil Rights",
    3:  "First Amendment",
    4:  "Due Process",
    5:  "Privacy",
    6:  "Attorneys",
    7:  "Unions",
    8:  "Economic Activity",
    9:  "Judicial Power",
    10: "Federalism",
    11: "Interstate Relations",
    12: "Federal Taxation",
    13: "Miscellaneous",
    14: "Private Action",
    0:  "Unclassified",
}

# Keywords in shadow docket cases that translate into Spaeth Issue Areas
keywordmap = [

    # Criminal Procedure
    # Includes death penalty, habeas corpus, stay of execution, miranda, search and seizure, and right to counsel.
    (1, ["execution", "sentence of death", "death penalty", "lethal injection",
         "stay of execution", "capital punishment", "death row",
         "habeas corpus", "habeas",
         "miranda", "search and seizure", "right to counsel",
         "cruel and unusual", "double jeopardy", "self-incrimination",
         "speedy trial", "jury trial", "plea bargain",
         "involuntary confession", "confrontation clause",
         "sentencing guideline", "firearms", "narcotics",
         "bank robbery", "obstruction of justice"]),

    # Civil Rights
    # Includes voting/VRA, desegregation, employment discrimination, affirmative action, sex discrimination, immigration/naturalization, deportation, indigents, and military.
    (2, ["voting rights", "voting rights act", "reapportionment", "redistrict",
         "gerrymandering", "ballot access", "desegregation",
         "employment discrimination", "affirmative action",
         "sex discrimination", "gender discrimination",
         "race discrimination", "racial discrimination",
         "equal protection", "civil rights act",
         "immigration and naturalization", "immigr", "deportation", "deport",
         "removal order", "asylum", "alienage", "employability of alien",
         "daca", "title 42", "remain in mexico",
         "gonzales, attorney general", "gonzalez, attorney general",
         "stay of removal",
         "indigent", "appointment of counsel",
         "americans with disabilities", "ada ",
         "handicapped", "poverty law",
         "election", "voter", "ballot", "electoral",
         "secretary of state", "blackwell"]),

    # First Amendment
    # Includes free exercise, establishment, parochiaid, commercial speech, libel, protest, campaign spending, and obscenity.
    (3, ["first amendment", "free exercise", "establishment clause",
         "establishment of religion", "parochiaid", "religious school",
         "free speech", "freedom of speech", "commercial speech",
         "libel", "defamation", "protest demonstration", "campaign spending",
         "obscenity", "conscientious objector", "loyalty oath",
         "religion", "religious", "church", "mosque", "prayer",
         "bible", "uniao do vegetal", "o centro"]),

    # Due Process
    # Includes prisoners' rights, takings clause, hearing or notice, and impartial decision maker.
    (4, ["due process", "prisoners' rights", "prisoner rights",
         "takings clause", "taking of property", "just compensation",
         "hearing or notice", "impartial decision"]),

    # Privacy
    # Includes abortion and right to die (Spaeth is narrow).
    (5, ["abort", "contracepti", "planned parenthood", "dobbs", "roe v. wade",
         "mifepristone", "medication abortion",
         "right to die", "freedom of information act", "foia"]),

    # Attorneys
    (6, ["attorney discipline", "bar admission", "disbarment",
         "admission to the bar", "attorney's fees", "attorney fees"]),

    # Unions
    (7, ["labor union", "union activity", "collective bargaining",
         "fair labor standards", "labor-management", "picketing",
         "secondary boycott", "closed shop", "agency shop"]),

    # Economic Activity
    # Includes antitrust, bankruptcy, environmental/natural resources, state/local regulation, patents, securities, transportation, and public utilities.
    (8, ["antitrust", "merger", "bankruptcy",
         "environmental", "natural resources", "clean air", "clean water",
         "emissions", "endangered species", "pipeline", "natural gas",
         "epa", "army corps", "pollution",
         "state regulation of business", "public utilities",
         "patent", "copyright", "trademark",
         "securities", "railroad", "airline", "motor carrier",
         "nuclear power", "oil producer", "cable television",
         "telephone", "telegraph",
         "workers compensation", "tort action", "punitive damages",
         "liability", "arbitration", "consumer protection",
         "zoning", "government corruption",
         "exxon", "ppg industries"]),

    # Judicial Power
    # Includes comity/abstention, standing, federal court jurisdiction, and extraordinary relief/mandamus.
    (9, ["standing to sue", "mootness", "ripeness",
         "jurisdiction of", "federal court jurisdiction",
         "circuit court", "court of appeals jurisdiction",
         "mandamus", "extraordinary relief",
         "comity", "abstention", "exhaustion of remedies",
         "res judicata", "collateral estoppel",
         "federal rules of civil procedure", "diversity jurisdiction",
         "certiorari jurisdiction"]),

    # Federalism
    # Includes federal preemption, national supremacy, and federal-state ownership.
    (10, ["federal pre-emption", "federal preemption", "preemption",
          "supremacy clause", "national supremacy",
          "eleventh amendment", "sovereign immunity",
          "federal-state", "submerged lands"]),

    # Interstate Relations
    (11, ["boundary dispute", "interstate compact", "dispute between states"]),

    # Federal Taxation
    (12, ["internal revenue", "federal tax", "income tax",
          "gift tax", "irs ", "tax court"]),

    # Miscellaneous
    # Includes legislative veto and executive authority vis-a-vis congress.
    (13, ["legislative veto", "executive authority", "separation of powers",
          "osha", "cdc", "pandemic", "covid", "vaccine", "mask mandate",
          "eviction moratorium",
          "guantanamo", "enemy combatant", "military tribunal",
          "detain", "detention",
          "material support terrorism",
          "military", "defense", "base closure", "rumsfeld",
          "armed forces", "national security",
          "gherebi", "padilla"]),

    # Private Action
    (14, ["real property", "personal property", "contract dispute",
          "wills and trusts", "commercial transaction",
          "divorce", "custody", "sibley", "schiavo",
          "civil procedure"]),
]


def categorize(text):
    """
    Return (spaeth_code, label) for the first keyword match.
    Falls back to (0, 'Unclassified') if nothing matches.
    """
    if pd.isna(text):
        return 0, "Unclassified"
    t = text.lower()
    for code, keywords in keywordmap:
        if any(kw in t for kw in keywords):
            return code, issuearealabels[code]
    return 0, "Unclassified"


# Load & Prep data
print("Loading data...")
df = pd.read_csv(shadowdocketdata, encoding="latin1", low_memory=False)
ea = df[(df["emergency_application"] == 1.0) & (df["term"] == 2020)].copy()
print(f"  Shadow docket emergency applications (2020 Term): {len(ea):,}")

scdb = pd.read_csv(scdbdata, encoding="latin1")
merits = scdb[scdb["term"] == 2020].copy()
merits["spaeth_label"] = merits["issueArea"].map(issuearealabels).fillna("Unclassified")
print(f"  Merits docket decisions (2020 Term): {len(merits):,}")

sal = pd.read_excel(saliencedata)
sal["Article Count"] = pd.to_numeric(sal["Article Count"], errors="coerce").fillna(0)
sal_shadow = sal[sal["Docket Type"] == "Shadow"].copy()
sal_merits = sal[sal["Docket Type"] == "Merits"].copy()
print(f"  Salience scores loaded: {len(sal_shadow)} shadow, {len(sal_merits)} merits\n")

# Merge salience scores
ea["docket_number"] = ea["docket_number"].astype(str).str.strip()
sal_shadow["docket_number"] = sal_shadow["Docket Number"].astype(str).str.strip()
ea = ea.merge(
    sal_shadow[["docket_number", "Article Count"]].rename(columns={"Article Count": "salience"}),
    on="docket_number", how="left"
).fillna({"salience": 0})

merits["docket"] = merits["docket"].astype(str).str.strip()
sal_merits["docket"] = sal_merits["Docket Number"].astype(str).str.strip()
merits = merits.merge(
    sal_merits[["docket", "Article Count"]].rename(columns={"Article Count": "salience"}),
    on="docket", how="left"
).fillna({"salience": 0})

# Categorize shadow docket
results = ea["text"].apply(categorize)
ea["spaeth_code"]  = results.apply(lambda x: x[0])
ea["spaeth_label"] = results.apply(lambda x: x[1])
ea["granted_bin"]  = (ea["relief"] == "Granted").astype(int)
ea["high_sal"]     = ea["spaeth_label"].isin(highsalienceareas).astype(int)
merits["high_sal"] = merits["spaeth_label"].isin(highsalienceareas).astype(int)


# TABLE 1 — Issue area distribution: shadow vs merits
print("=" * 65)
print("TABLE 1 — Issue Area Distribution: Shadow vs Merits (2020 Term)")
print("=" * 65)
shadowcounts = ea["spaeth_label"].value_counts().rename("Shadow N")
meritscounts = merits["spaeth_label"].value_counts().rename("Merits N")
dist = pd.concat([shadowcounts, meritscounts], axis=1).fillna(0).astype(int)
dist["Shadow %"] = (dist["Shadow N"] / len(ea) * 100).round(1)
dist["Merits %"] = (dist["Merits N"] / len(merits) * 100).round(1)
dist["High Salience"] = ["YES" if i in highsalienceareas else "" for i in dist.index]
dist = dist.sort_values("Merits N", ascending=False)
print(dist.to_string())


# TABLE 2 — High-salience summary by docket type
print("\n" + "=" * 65)
print("TABLE 2 — High-Salience Cases by Docket Type (2020 Term)")
print("=" * 65)
print(f"\nHigh-salience areas: {highsalienceareas}\n")
print(f"{'Docket':<10} {'Total':>8} {'High Sal N':>12} {'High Sal %':>12} {'Mean Articles':>15} {'Median Articles':>17}")
for label, data in [("Shadow", ea), ("Merits", merits)]:
    n = len(data)
    hs = data["high_sal"].sum()
    pct = hs / n * 100
    mean_sal = data["salience"].mean()
    med_sal = data["salience"].median()
    print(f"{label:<10} {n:>8} {hs:>12} {pct:>11.1f}% {mean_sal:>15.1f} {med_sal:>17.1f}")


# TABLE 3 — High-salience issue areas: shadow vs merits breakdown
print("\n" + "=" * 65)
print("TABLE 3 — High-Salience Issue Areas: Shadow vs Merits")
print("=" * 65)
for area in highsalienceareas:
    s_n   = len(ea[ea["spaeth_label"] == area])
    s_pct = s_n / len(ea) * 100
    m_n   = len(merits[merits["spaeth_label"] == area])
    m_pct = m_n / len(merits) * 100
    s_sal = ea[ea["spaeth_label"] == area]["salience"].mean() if s_n > 0 else 0
    m_sal = merits[merits["spaeth_label"] == area]["salience"].mean() if m_n > 0 else 0
    print(f"\n  {area}")
    print(f"    Shadow: {s_n} cases ({s_pct:.1f}%) | mean salience {s_sal:.1f} articles")
    print(f"    Merits: {m_n} cases ({m_pct:.1f}%) | mean salience {m_sal:.1f} articles")


# TABLE 4 — Grant and dissent rates for shadow docket cases by issue area
print("\n" + "=" * 65)
print("TABLE 4 — Shadow Docket: Grant & Dissent Rates by Issue Area")
print("=" * 65)
shadowsummary = (
    ea.groupby("spaeth_label")
    .agg(
        n=("granted_bin", "count"),
        granted=("granted_bin", "sum"),
        dissents=("dissent", "sum"),
        mean_salience=("salience", "mean"),
    )
    .assign(
        grant_pct=lambda x: (x["granted"] / x["n"] * 100).round(1),
        dissent_pct=lambda x: (x["dissents"] / x["n"] * 100).round(1),
    )
    .sort_values("n", ascending=False)
)
shadowsummary["High Salience"] = ["YES" if i in highsalienceareas else "" for i in shadowsummary.index]
print(shadowsummary.round(1).to_string())