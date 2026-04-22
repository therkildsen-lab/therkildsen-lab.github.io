#! /usr/bin/env python3

from datetime import datetime, timezone
import requests
import time
import xml.etree.ElementTree as ET

ORCID_ID = "0000-0002-6591-591X"
YOUR_EMAIL = "pd348@cornell.edu"      # polite identifier for the doi.org API
ORCID_API_URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
listlink = '<p>Full list available <a href="https://scholar.google.com/citations?hl=en&user=MT9QVi4AAAAJ&view_op=list_works&sortby=pubdate">here</p>'
MD_HEADER = f"""+++
title = "Publications"
template = "custom_page.html"
[[extra.content_blocks]]
block = "page-heading"
title = "Lab Publications"
[[extra.content_blocks]]
block = "content"
content_html = \"\"\"{listlink}\n
"""

def fetch_works():
    headers = {"Accept": "application/json"}
    r = requests.get(ORCID_API_URL, headers=headers)
    r.raise_for_status()
    return r.json().get("group", [])

def fetch_doi_metadata(doi):
    """Fetch full citation metadata from doi.org, including authors."""
    url = f"https://dx.doi.org/{doi}"
    headers = {
        "Accept": "application/citeproc+json",
        "User-Agent": f"mailto:{YOUR_EMAIL}",
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()
    return None

def format_authors(doi_meta):
    authors = doi_meta.get("author", [])
    parts = []
    for a in authors:
        family = a.get("family", "")
        given = a.get("given", "")
        # Format as "Family AB" (last name + initials)
        initials = "".join(w[0] for w in given.split()) if given else ""
        parts.append(f"{family} {initials}".strip())
    return ", ".join(parts)

def extract_doi(summary):
    for ext_id in summary.get("external-ids", {}).get("external-id", []):
        if ext_id.get("external-id-type") == "doi":
            return ext_id.get("external-id-value", "").strip()
    return None

def build_feed_and_page(works):
    ET.register_namespace("", "http://www.w3.org/2005/Atom")
    feed = ET.Element("{http://www.w3.org/2005/Atom}feed")

    def sub(parent, tag, text=None, **attrib):
        el = ET.SubElement(parent, f"{{http://www.w3.org/2005/Atom}}{tag}", **attrib)
        if text:
            el.text = text
        return el

    sub(feed, "title", "Lab Publications")
    sub(feed, "id", f"https://orcid.org/{ORCID_ID}")
    sub(feed, "updated", datetime.now(timezone.utc).isoformat())
    sub(feed, "link", href=f"https://orcid.org/{ORCID_ID}", rel="alternate")

    page_entries = []

    for group in works:
        summary = group.get("work-summary", [{}])[0]
        title = summary.get("title", {}).get("title", {}).get("value", "Untitled")
        pub_date = summary.get("publication-date") or {}
        year = (pub_date.get("year") or {}).get("value", "")
        doi = extract_doi(summary)
        doi_url = f"https://doi.org/{doi}" if doi else summary.get("url", {}).get("value") or f"https://orcid.org/{ORCID_ID}"
        work_id = summary.get("put-code", "")
        journal = summary.get("journal-title", {}).get("value", "") if summary.get("journal-title") else ""

        # Try to enrich with doi.org metadata for authors
        authors = ""
        if doi:
            doi_meta = fetch_doi_metadata(doi)
            if doi_meta:
                authors = format_authors(doi_meta)
                # Prefer doi.org journal name if ORCID didn't have one
                if not journal:
                    journal = doi_meta.get("container-title", [""])[0] if doi_meta.get("container-title") else ""
            time.sleep(0.5)

        # Build Atom feed entry
        entry = sub(feed, "entry")
        sub(entry, "title", title)
        sub(entry, "id", f"https://orcid.org/{ORCID_ID}/work/{work_id}")
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
            title_bold = f"<strong>{e['title']}.</strong> " if e['title'] else ""
            year = f"{e['year']}. " if e['year'] else ""
            journal = f"{e['journal']}. " if e['journal'] else ""
            doi_link = f'<a href="{e["doi_url"]}">{e["doi"]}</a>' if e['doi'] else ""
            f.write(f"<p>- {authors}{title_bold}{year}{journal}{doi_link}</p>\n")
        f.write("\"\"\"\n\n+++")

if __name__ == "__main__":
    works = fetch_works()
    tree, feed_element, page_entries = build_feed_and_page(works)
    ET.indent(tree)
    tree.write("static/publications.xml", encoding="unicode", xml_declaration=True)
    print(f"Feed written with {len(works)} entries.")
    build_publications_page(page_entries)
    print("Publications page written to content/publications.md.")