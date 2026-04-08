"""
fetch_publications.py
Fetches publications for Viviane Tenório from the Semantic Scholar API
and writes them to _data/publications.yml for the Jekyll site.

Runs automatically via GitHub Actions every Monday.
To run manually: python scripts/fetch_publications.py
"""

import requests
import yaml
import json
from datetime import date
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────
AUTHOR_NAME = "Viviane Tenório"
# Semantic Scholar author search — update AUTHOR_ID once confirmed
# To find your ID: https://api.semanticscholar.org/graph/v1/author/search?query=viviane+tenorio+neuroscience
AUTHOR_ID = None  # Set this once you have confirmed your Semantic Scholar ID

# Fallback: known DOIs to always include (manual seed list)
KNOWN_DOIS = [
    "10.1109/SBESC49506.2019.9046097",
    "10.1109/INSCIT.2019.8868453",
    "10.1109/IWSSIP48289.2020.9145352",
]

EXTRA_PAPERS = [
    {
        "title": "Rotational dynamics in subcortical systems during reach",
        "authors": "Tenório, V.S.G.M., Baker, S.N.",
        "venue": "UK Sensorimotor Conference",
        "year": 2025,
        "type": "conference",
        "tags": ["dynamical systems", "reticular formation", "motor cortex", "jPCA"],
    },
    {
        "title": "Applying a Dynamical Systems Approach to Neural Recordings from Cortical and Sub-cortical Motor Centres in Awake Behaving Monkeys",
        "authors": "Tenório, V.S.G.M., Baker, S.N.",
        "venue": "UK Sensorimotor Conference, Aston University",
        "year": 2022,
        "type": "conference",
        "tags": ["dynamical systems", "motor control", "electrophysiology", "jPCA"],
    },
]

OUTPUT_PATH = Path("_data/publications.yml")

# ── Tag inference ───────────────────────────────────────────────
NEURO_KEYWORDS = ["motor", "neural", "cortex", "brainstem", "reticular",
                  "neuroscience", "movement", "electrophysiology", "dynamical",
                  "brain", "spike", "seizure", "epilepsy", "EEG", "jPCA"]
ENG_KEYWORDS = ["IoT", "FPGA", "embedded", "sensor", "signal", "instrumentation",
                "cybersecurity", "radiometer", "confidentiality", "network"]

def infer_tags(title, venue=""):
    combined = (title + " " + venue).lower()
    tags = []
    for k in NEURO_KEYWORDS:
        if k.lower() in combined:
            tags.append(k.lower())
    for k in ENG_KEYWORDS:
        if k.lower() in combined:
            tags.append(k.lower())
    return list(set(tags))[:6]  # cap at 6 tags

# ── Fetch from Semantic Scholar by DOI ─────────────────────────
def fetch_by_doi(doi):
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
    params = {"fields": "title,authors,venue,year,publicationTypes,externalIds"}
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"  Warning: could not fetch DOI {doi}: {e}")
    return None

def fetch_by_author_id(author_id):
    url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers"
    params = {"fields": "title,authors,venue,year,publicationTypes,externalIds", "limit": 50}
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            return r.json().get("data", [])
    except Exception as e:
        print(f"  Warning: could not fetch author papers: {e}")
    return []

def paper_to_dict(paper, doi=None):
    authors_list = paper.get("authors", [])
    authors_str = ", ".join(a.get("name", "") for a in authors_list[:4])
    if len(authors_list) > 4:
        authors_str += " et al."

    pub_types = paper.get("publicationTypes") or []
    pub_type = "conference" if any("Conference" in t for t in pub_types) else "journal"

    external = paper.get("externalIds") or {}
    resolved_doi = doi or external.get("DOI")

    title = paper.get("title", "")
    venue = paper.get("venue", "")
    year = paper.get("year") or 0

    entry = {
        "title": title,
        "authors": authors_str,
        "venue": venue,
        "year": year,
        "type": pub_type,
        "tags": infer_tags(title, venue),
    }
    if resolved_doi:
        entry["doi"] = resolved_doi
    return entry

# ── Main ────────────────────────────────────────────────────────
def main():
    papers = []
    seen_titles = set()

    print("Fetching publications from Semantic Scholar...")

    # 1. Fetch by author ID if available
    if AUTHOR_ID:
        print(f"  Fetching by author ID: {AUTHOR_ID}")
        raw = fetch_by_author_id(AUTHOR_ID)
        for p in raw:
            entry = paper_to_dict(p)
            key = entry["title"].lower().strip()
            if key not in seen_titles:
                papers.append(entry)
                seen_titles.add(key)
        print(f"  Found {len(papers)} papers via author ID")

    # 2. Fetch by known DOIs
    for doi in KNOWN_DOIS:
        print(f"  Fetching DOI: {doi}")
        raw = fetch_by_doi(doi)
        if raw:
            entry = paper_to_dict(raw, doi=doi)
            key = entry["title"].lower().strip()
            if key not in seen_titles:
                papers.append(entry)
                seen_titles.add(key)

    # 3. Merge manually curated extras (conference abstracts not in Semantic Scholar)
    for extra in EXTRA_PAPERS:
        key = extra["title"].lower().strip()
        if key not in seen_titles:
            papers.append(extra)
            seen_titles.add(key)

    # 4. Sort by year descending
    papers.sort(key=lambda p: p.get("year", 0), reverse=True)

    print(f"Total publications: {len(papers)}")

    # 5. Write YAML
    header = f"# Auto-updated by scripts/fetch_publications.py\n# Last updated: {date.today()}\n\n"
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.dump(papers, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=False, indent=2)

    print(f"Written to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
