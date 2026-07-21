# Samvardhini's real publications page

Goal: build an interactive HTML page of Samvardhini Sridharan's own published papers, with
charts of how citations have grown over time, and publish it live via GitHub Pages.

This replaces the sample-data walkthrough (see TODO-20260721-page.md) with Samvardhini's real
ORCID and papers, now that the workflow has been proven out.

## Steps
- [x] Confirm ORCID: `0000-0002-2224-4124` (Samvardhini Sridharan) — verified by Samvardhini opening
  the ORCID record directly
- [x] Fetch and verify papers
- [x] Design the page for a short list (interview, then plan)
- [x] Build/update index.html and papers.json with real data
- [ ] Refine the look
- [ ] Publish live with GitHub Pages

## Design plan (from interview)
- **Focus:** personal narrative/timeline, not a dense CV list — 3 papers, chronological, each with
  a short story blurb
- **Style:** warm & personal
- **Colors:** UW purple stays as the primary accent; each paper gets its own color so they can be
  tracked/toggled individually:
  - Nat Comms 2026 (genomics, most recent) → UW purple `#4b2e83` / dark `#9d8fd0`
  - arXiv 2020 (ultrasound navigation) → terracotta `#b5563a` / dark `#d98a6f`
  - eScholarship 2019 (breast cancer radiomics) → teal `#1f7a6c` / dark `#4bab99`
- **Bio line (draft, editable):** "From medical imaging to population genomics — exploring how
  structural variation shapes human and primate genomes, after starting out building real-time
  navigation tools for cancer imaging."
- **Chart:** one interactive per-year citations line chart, one line per paper in its own color.
  Legend chips above the chart act as toggles: clicking a chip shows/hides that paper's line AND
  scrolls to/highlights its blurb card in the timeline below. No cumulative or papers-per-year
  charts this time — too sparse to be meaningful with 3 papers.
- **Timeline cards (draft blurbs, editable):**
  1. 2026, Nature Communications — "My most recent work, published in Nature Communications, maps
     recurring structural variation at a hotspot on chromosome 17 across humans and great apes —
     part of the Sudmant Lab's work on genome evolution."
  2. 2020, arXiv — "Early in my research career, I helped evaluate a real-time optical-tracking
     navigation system for contrast-enhanced ultrasound imaging, aimed at improving how clinicians
     track tumors during scans."
  3. 2019, eScholarship — "My first paper explored novel radiomics techniques for early breast
     cancer detection using ultrasonography — the start of my interest in imaging and quantitative
     biology."
- **Dark mode:** toggle included, same as the sample page

## Notes
- ORCID `0000-0002-2224-4124` has no works linked yet in OpenAlex, so fetch_papers.py (ORCID-based)
  found nothing. Had to locate papers by name search instead, which surfaced a real identity
  collision: an OpenAlex author profile "S. SRIDHARAN" merges Samvardhini's 2025-2026 genomics
  paper with an unrelated physical chemist's 1977-1981 papers on deuterium isotope effects
  (impossible timeline overlap — different person). Excluded those.
- Final verified list, 3 papers:
  1. "Recurrent structural variation and recent turnover at the 17q21.31 locus in humans and
     great apes" — Nature Communications, 2026 (kept over its bioRxiv preprint, same paper)
  2. "Clinical Evaluation of Real-Time Optical-Tracking Navigation and Live Time-Intensity
     Curves..." — arXiv, 2020 (preprint, no published version found)
  3. "Early Breast Cancer Detection via Novel Radiomics Techniques and Ultrasonography" —
     eScholarship, 2019
- Excluded: the Zenodo software release (sudmantlab/17q21.31_SV_and_evolution) tied to the Nat
  Comms paper — Samvardhini wants papers only, not code releases.
- Data saved to `my_papers.json` / `my_papers_review.csv` (kept separate from the sample data's
  `papers.json` / `papers_review.csv` from the walkthrough).
- Design being rethought from scratch for this short, 3-paper, cross-disciplinary list rather
  than reusing the sample page's academic/classic design as-is.
