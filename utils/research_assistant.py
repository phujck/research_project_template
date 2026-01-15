import argparse
import arxiv
import os
import datetime

def clean_filename(s):
    return "".join([c for c in s if c.isalpha() or c.isdigit() or c==' ']).rstrip().replace(" ", "_")

def generate_citekey(result):
    author = result.authors[0].name.split(" ")[-1]
    year = result.published.year
    return f"{clean_filename(author)}{year}"

def main():
    parser = argparse.ArgumentParser(description="Research Assistant: Fetch papers from arXiv.")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--max", type=int, default=3, help="Max results")
    args = parser.parse_args()

    # Directories
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    papers_dir = os.path.join(base_dir, "literature", "papers")
    reviews_dir = os.path.join(base_dir, "literature", "reviews")
    bib_file = os.path.join(base_dir, "literature", "bibliography.bib")

    os.makedirs(papers_dir, exist_ok=True)
    os.makedirs(reviews_dir, exist_ok=True)

    client = arxiv.Client()
    search = arxiv.Search(
        query=args.query,
        max_results=args.max,
        sort_by=arxiv.SortCriterion.Relevance
    )

    print(f"Searching for '{args.query}'...")
    
    new_entries = []

    for result in client.results(search):
        citekey = generate_citekey(result)
        pdf_filename = f"{citekey}.pdf"
        pdf_path = os.path.join(papers_dir, pdf_filename)
        review_path = os.path.join(reviews_dir, f"{citekey}.md")

        print(f"Found: {result.title} ({citekey})")

        # 1. Download PDF
        if not os.path.exists(pdf_path):
            print(f"  Downloading to {pdf_filename}...")
            result.download_pdf(dirpath=papers_dir, filename=pdf_filename)
        else:
            print("  PDF already exists.")

        # 2. Update Bibliography
        bib_entry = f"""
@article{{{citekey},
    title = {{{result.title}}},
    author = {{{' and '.join([a.name for a in result.authors])}}},
    year = {{{result.published.year}}},
    journal = {{arXiv:{result.entry_id.split('/')[-1]}}},
    url = {{{result.entry_id}}}
}}
"""
        # Simple duplicaton check
        if os.path.exists(bib_file):
            with open(bib_file, 'r', encoding='utf-8') as f:
                if citekey in f.read():
                    pass # Already exists
                else:
                    new_entries.append(bib_entry)
        else:
            new_entries.append(bib_entry)

        # 3. Create Review Stub
        if not os.path.exists(review_path):
            with open(review_path, 'w', encoding='utf-8') as f:
                f.write(f"""---
citekey: "{citekey}"
title: "{result.title}"
authors: {[a.name for a in result.authors]}
year: {result.published.year}
venue: "arXiv"
status: "Inbox"
tags: []
---

# Abstract
{result.summary}

# key Findings
(To be filled)

# Methodology
(To be filled)
""")
            print(f"  Created review stub at {review_path}")

    # Append new bib entries
    if new_entries:
        with open(bib_file, 'a', encoding='utf-8') as f:
            for entry in new_entries:
                f.write(entry)
        print(f"Added {len(new_entries)} entries to bibliography.")

if __name__ == "__main__":
    main()
