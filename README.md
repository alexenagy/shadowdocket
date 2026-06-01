# Shadow Docket Analysis

This repository contains the code and data used in an exploratory analysis of issue area distribution across the Supreme Court's merits and shadow dockets in the 2020 Term. The analysis was conducted as part of a paper examining whether high-salience issue areas are disproportionately resolved through the shadow docket outside the Court's conventional deliberative process.

## Files

### Code
- `categorize_shadow_docket.py` — Main analysis script. Classifies shadow docket emergency applications by Spaeth issue area using a keyword-based coding scheme, merges media salience scores, and produces cross-docket comparison tables for the 2020 Term.

### Data (included)
- `data/SCDB_2025_01_caseCentered_Citation.csv` — Supreme Court Database case-centered citation file (Spaeth et al. 2025). Downloaded from [scdb.wustl.edu](http://scdb.wustl.edu).
- `data/issuesalience.xlsx` — Original media salience dataset constructed using NexisUni article counts for all 115 cases in the 2020 Term across both dockets.

### Data (not included — download separately)
- `data/shadow_docket_database_v2-0.csv` — Kastellec and Taboni shadow docket database (2026). Too large for GitHub. Download from the *Journal of Law and Courts* replication materials or contact the authors directly.

## Requirements

```
pandas
openpyxl
```

Install with:

```bash
pip install pandas openpyxl
```

## Usage

Place all data files in a `data/` subfolder, then run:

```bash
python3 categorize_shadow_docket.py
```

## Data Sources

- Kastellec, Jonathan P., and Anthony R. Taboni. 2026. "A Database of the United States Supreme Court's Shadow Docket, 1993–2025." *Journal of Law and Courts* 14 (1): 220–237.
- Spaeth, Harold J., Lee Epstein, Andrew D. Martin, Jeffrey A. Segal, Theodore J. Ruger, and Sara C. Benesh. 2025. *The Supreme Court Database, Version 2025 Release 01*. Washington University in St. Louis. [scdb.wustl.edu](http://scdb.wustl.edu).
- Salience data collected via NexisUni using the method adapted from Epstein and Segal (2000) and Clark, Lax, and Rice (2015).