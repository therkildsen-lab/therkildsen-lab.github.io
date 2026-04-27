#! /usr/bin/env python3

from datetime import datetime, timezone
import requests
import xml.etree.ElementTree as ET

AUTHOR_ID = "6035178"
AUTHOR_NAME = "N. Therkildsen"
S2_API_BASE = "https://api.semanticscholar.org/graph/v1"
FIELDS = "title,year,journal,externalIds,authors"

MD_HEADER = """+++
title = "Publications"
template = "custom_md.html"
[[extra.content_blocks]]
block = "page-heading"
title = "Lab Publications"
+++

"""

def fetch_works():
    """Fetch all papers for the author from Semantic Scholar."""
    papers = []
    offset = 0
    limit = 100

    while True:
        url = (
            f"{S2_API_BASE}/author/{AUTHOR_ID}/papers"
            f"?fields={FIELDS}&limit={limit}&offset={offset}"
        )
        r = requests.get(url, headers={"User-Agent": "mailto:pd348@cornell.edu"})
        r.raise_for_status()
        data = r.json()

        batch = data.get("data", [])
        papers.extend(batch)

        # Stop if we've fetched everything
        if len(batch) < limit:
            break
        offset += limit

    # Sort by year descending
    papers.sort(key=lambda p: p.get("year") or 0, reverse=True)
    return papers


def format_authors(authors):
    """Format author list as 'Family AB, Family CD, ...'"""
    parts = []
    for a in authors:
        name = a.get("name", "")
        # Semantic Scholar gives full names; abbreviate given name to initials
        name_parts = name.strip().split()
        if len(name_parts) >= 2:
            family = name_parts[-1]
            initials = "".join(p[0] for p in name_parts[:-1])
            parts.append(f"{family} {initials}")
        else:
            parts.append(name)
    return ", ".join(parts)


def build_feed_and_page(papers):
    ET.register_namespace("", "http://www.w3.org/2005/Atom")
    feed = ET.Element("{http://www.w3.org/2005/Atom}feed")

    def sub(parent, tag, text=None, **attrib):
        el = ET.SubElement(parent, f"{{http://www.w3.org/2005/Atom}}{tag}", **attrib)
        if text:
            el.text = text
        return el

    sub(feed, "title", "Lab Publications")
    sub(feed, "id", f"https://www.semanticscholar.org/author/{AUTHOR_ID}")
    sub(feed, "updated", datetime.now(timezone.utc).isoformat())
    sub(feed, "link", href=f"https://www.semanticscholar.org/author/{AUTHOR_ID}", rel="alternate")

    page_entries = []

    for paper in papers:
        title = paper.get("title") or "Untitled"
        year = str(paper.get("year") or "")
        authors = format_authors(paper.get("authors", []))
        journal = (paper.get("journal") or {}).get("name", "")
        external_ids = paper.get("externalIds") or {}
        doi = external_ids.get("DOI", "")
        paper_id = paper.get("paperId", "")

        doi_url = f"https://doi.org/{doi}" if doi else f"https://www.semanticscholar.org/paper/{paper_id}"

        # Atom feed entry
        entry = sub(feed, "entry")
        sub(entry, "title", title)
        sub(entry, "id", f"https://www.semanticscholar.org/paper/{paper_id}")
        sub(entry, "updated", f"{year}-01-01T00:00:00+00:00" if year else datetime.now(timezone.utc).isoformat())
        sub(entry, "link", href=doi_url, rel="alternate")

        page_entries.append({
            "authors": authors,
            "title": title,
            "year": year,
            "journal": journal,
            "doi_url": doi_url,
            "doi": doi,
        })

    return ET.ElementTree(feed), feed, page_entries


def build_publications_page(page_entries):
    with open("content/publications.md", "w") as f:
        f.write(MD_HEADER)
        for e in page_entries:
            authors = f"{e['authors']}. " if e['authors'] else ""
            title_bold = f"**{e['title']}.** " if e['title'] else ""
            title_bold.replace("..", ".")
            year = f"{e['year']}. " if e['year'] else ""
            journal = f"{e['journal']}. " if e['journal'] else ""
            doi_link = f'[{e["doi"]}]({e["doi_url"]})' if e['doi'] else ""
            if doi_link:
                f.write(f"- {authors}{title_bold}{year}{journal}{doi_link}\n")


if __name__ == "__main__":
    print("Fetching papers from Semantic Scholar...")
    papers = fetch_works()
    print(f"Found {len(papers)} papers.")

    tree, feed_element, page_entries = build_feed_and_page(papers)
    #ET.indent(tree)
    #tree.write("static/publications.xml", encoding="unicode", xml_declaration=True)
    #print("Feed written to static/publications.xml.")

    build_publications_page(page_entries)
    print("Publications page written to content/publications.md.")