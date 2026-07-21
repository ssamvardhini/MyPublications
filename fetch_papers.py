#!/usr/bin/env python3
"""Fetch a researcher's works from OpenAlex by ORCID and save papers.json + a review spreadsheet.

Usage:
    python3 -X utf8 fetch_papers.py <ORCID> [--email you@example.com]

Run with `-X utf8` so special characters in titles/names (e.g. Greek letters) write cleanly.
"""

import argparse
import csv
import json
import sys
import time
from pathlib import Path

import requests

OPENALEX_WORKS_URL = "https://api.openalex.org/works"


def fetch_all_works(orcid: str, email: str | None) -> list[dict]:
    headers = {"User-Agent": f"mailto:{email}" if email else "MyPublications-fetch-script"}
    works = []
    cursor = "*"
    while cursor:
        params = {
            "filter": f"authorships.author.orcid:{orcid}",
            "per-page": 200,
            "cursor": cursor,
        }
        for attempt in range(5):
            resp = requests.get(OPENALEX_WORKS_URL, params=params, headers=headers, timeout=30)
            if resp.status_code == 429:
                wait = 2 ** attempt
                print(f"  Rate limited by OpenAlex, waiting {wait}s and retrying...", file=sys.stderr)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            break
        else:
            raise RuntimeError("OpenAlex kept rate-limiting after several retries")

        data = resp.json()
        works.extend(data["results"])
        cursor = data.get("meta", {}).get("next_cursor")
        if not data["results"]:
            break
    return works


def simplify(work: dict) -> dict:
    venue = None
    if work.get("primary_location") and work["primary_location"].get("source"):
        venue = work["primary_location"]["source"].get("display_name")

    co_authors = [
        a["author"]["display_name"]
        for a in work.get("authorships", [])
        if a.get("author", {}).get("display_name")
    ]

    return {
        "id": work.get("id", "").rsplit("/", 1)[-1],
        "title": work.get("title") or work.get("display_name"),
        "year": work.get("publication_year"),
        "type": work.get("type"),
        "venue": venue,
        "cited_by_count": work.get("cited_by_count", 0),
        "counts_by_year": work.get("counts_by_year", []),
        "doi": work.get("doi"),
        "url": work.get("doi") or work.get("id"),
        "co_authors": co_authors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("orcid", help="ORCID, e.g. 0000-0002-9575-0255")
    parser.add_argument("--email", help="contact email for OpenAlex's polite pool (faster, more reliable)")
    parser.add_argument("--out-json", default="papers.json")
    parser.add_argument("--out-csv", default="papers_review.csv")
    args = parser.parse_args()

    print(f"Fetching works for ORCID {args.orcid} from OpenAlex...")
    raw_works = fetch_all_works(args.orcid, args.email)
    papers = [simplify(w) for w in raw_works]
    papers.sort(key=lambda p: (p["year"] or 0), reverse=True)

    out_dir = Path(__file__).parent
    with open(out_dir / args.out_json, "w", encoding="utf-8") as f:
        json.dump({"meta": {"orcid": args.orcid, "source": "OpenAlex", "count": len(papers)}, "papers": papers}, f, indent=2, ensure_ascii=False)

    with open(out_dir / args.out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "year", "venue", "type", "co_authors"])
        for p in papers:
            writer.writerow([p["title"], p["year"], p["venue"], p["type"], "; ".join(p["co_authors"])])

    by_type: dict[str, int] = {}
    for p in papers:
        by_type[p["type"]] = by_type.get(p["type"], 0) + 1

    print(f"\nSaved {len(papers)} works to {args.out_json} and {args.out_csv}")
    print("Breakdown by type:")
    for t, count in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {t}: {count}")


if __name__ == "__main__":
    main()
