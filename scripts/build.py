"""Build the MD³ website from the Markdown files in content/.

    python scripts/build.py            build into site/
    python scripts/build.py --serve    build, then preview at http://localhost:8000

Content lives in content/ (Markdown + a little YAML), page layouts in
templates/, styling in assets/style.css. See README.md.
"""
import datetime
import re
import shutil
import sys
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
OUT = ROOT / "site"


# --------------------------------------------------------------------- reading

def render_md(text):
    """Markdown -> HTML. 'extra' gives tables and {.class} attributes; 'smarty' curly quotes."""
    html = markdown.markdown(text or "", extensions=["extra", "smarty", "sane_lists"])
    return Markup(html)


def load(path):
    """Read a Markdown file with an optional YAML block between --- lines at the top."""
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if match:
        meta = yaml.safe_load(match.group(1)) or {}
        body = match.group(2)
    meta["slug"] = path.stem
    meta["body"] = body.strip()
    meta["html"] = render_md(body)
    return meta


def collection(folder):
    """Every .md file in content/<folder>/, except those starting with '_'."""
    files = sorted(p for p in (CONTENT / folder).glob("*.md") if not p.name.startswith("_"))
    return [load(p) for p in files]


def by_order(items):
    return sorted(items, key=lambda item: (item.get("order", 999), item["slug"]))


# ------------------------------------------------------------------- site data

site = yaml.safe_load((CONTENT / "site.yml").read_text(encoding="utf-8"))
pages = {slug: load(CONTENT / f"{slug}.md") for slug in ["home", *site["nav"]]}
site["nav"] = [{"slug": slug, "title": pages[slug].get("title", slug.title())} for slug in site["nav"]]
site["year"] = datetime.date.today().year

# Home heading: the capital initials (M, D, D, D) are wrapped so the stylesheet
# can colour them, which shows where "MD³" comes from.
pages["home"]["title_html"] = Markup(re.sub(
    r"\b([A-Z])", r'<span class="initial">\1</span>', str(escape(pages["home"]["title"]))))

# Research themes: the body may hold a "> quote" block, which is styled as a callout.
themes = by_order(collection("research"))

# People: text before the first "## heading" is the bio; the heading is the
# project title and everything after it describes the project.
people = by_order(collection("people"))
theme_titles = {theme["slug"]: theme["title"] for theme in themes}
for person in people:
    bio, heading, project = re.match(r"(.*?)(?:^##\s+(.+?)\s*$(.*))?\Z", person["body"], re.S | re.M).groups()
    person["bio_html"] = render_md(bio)
    person["project_title"] = heading
    person["project_html"] = render_md(project)
    person["theme_title"] = theme_titles.get(person.get("theme"))
    person["first_name"] = person["name"].split()[0]

# Publications: grouped by year, newest first; preprints listed separately.
publications = yaml.safe_load((CONTENT / "publications.yml").read_text(encoding="utf-8")) or []
highlight = pages["publications"].get("highlight_authors", [])
for pub in publications:
    authors = str(escape(pub["authors"]))
    for name in highlight:
        authors = authors.replace(str(escape(name)), f"<strong>{escape(name)}</strong>")
    pub["authors_html"] = Markup(authors)
    pub["type"] = pub.get("type", "article")
publications.sort(key=lambda pub: -int(pub["year"]))  # stable: file order kept within a year


def by_year(kind):
    groups = {}
    for pub in publications:
        if pub["type"] == kind:
            groups.setdefault(pub["year"], []).append(pub)
    return list(groups.items())


# News: newest first. `date` comes from the front matter (YYYY-MM-DD).
news = collection("news")
for item in news:
    date = item.get("date")
    if isinstance(date, str):
        date = datetime.date.fromisoformat(date)
    item["date"] = date
    item["date_text"] = f"{date.day} {date:%B %Y}" if date else ""
news.sort(key=lambda item: item["date"] or datetime.date.min, reverse=True)


# -------------------------------------------------------------------- building

def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets", ignore=shutil.ignore_patterns(".DS_Store"))
    (OUT / ".nojekyll").touch()

    env = Environment(loader=FileSystemLoader(ROOT / "templates"),
                      autoescape=select_autoescape(["html"]),
                      trim_blocks=True, lstrip_blocks=True)
    shared = dict(site=site, themes=themes, people=people, news=news,
                  publications=publications,
                  articles=by_year("article"), preprints=by_year("preprint"))

    for slug, page in pages.items():
        # Use templates/<slug>.html when it exists, otherwise the plain text page.
        name = f"{slug}.html" if (ROOT / "templates" / f"{slug}.html").exists() else "page.html"
        html = env.get_template(name).render(page=page, current=slug, **shared)
        target = "index.html" if slug == "home" else f"{slug}.html"
        (OUT / target).write_text(html, encoding="utf-8")
    print(f"Built {len(pages)} pages in {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        import functools
        import http.server
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        print("Preview at http://localhost:8000  (Ctrl+C to stop; re-run to rebuild)")
        http.server.ThreadingHTTPServer(("localhost", 8000), handler).serve_forever()
