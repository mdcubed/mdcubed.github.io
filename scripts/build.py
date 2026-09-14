"""Build the static site with Python 3; no third-party dependencies required."""
import json
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site"
data = json.loads((ROOT / "content.json").read_text())
OUT.mkdir(exist_ok=True)
shutil.copytree(ROOT / "assets", OUT / "assets", dirs_exist_ok=True)
e = lambda value: escape(str(value), quote=True)
pages = ["Research", "People", "Publications", "News", "Join", "Contact"]
INSTITUTION_URL = 'https://www.ku.dk/en'
DEPARTMENT_URL = 'https://drug.ku.dk/'
CPDSE_URL = 'https://cpdse.dk/'

def institution_link():
    return f'<a href="{INSTITUTION_URL}">{e(data["institution"])}</a>'

def department_link():
    return f'<a href="{DEPARTMENT_URL}">{e(data["department"])}</a>'

def profile_link(person):
    if person.get('linkedin'):
        return f'<a class="text-link" href="{e(person["linkedin"])}">LinkedIn ↗</a>'
    return ''

def cards():
    return '<div class="research-grid">' + ''.join(
        f'<article class="research-card"><span class="number">0{i}</span><h3>{e(item["title"])}</h3><p>{e(item["description"])}</p></article>'
        for i, item in enumerate(data['research'], 1)) + '</div>'

def contact():
    return f'<a class="button" href="mailto:{e(data["email"])}">Get in touch <span aria-hidden="true">↗</span></a>'

def published_example(theme):
    example = theme.get('published_example')
    if not example:
        return ''
    return f'<aside class="published-example"><h3>Building on published results</h3><p>{e(example["text"])}</p><a class="text-link" href="{e(example["url"])}">{e(example["label"])} ↗</a></aside>'

def research_content():
    themes = ''.join(
        f'<article class="research-theme" id="{e(theme["id"])}"><p class="eyebrow">Research theme 0{i}</p><h2>{e(theme["title"])}</h2>'
        + ''.join(f'<p>{e(paragraph)}</p>' for paragraph in theme['details']) + published_example(theme) + '</article>'
        for i, theme in enumerate(data['research'], 1))
    return f'<p class="lead">{e(data["intro"])}</p><div class="prose research-themes">{themes}<h2>Open science and training</h2><p>Our research program emphasizes reproducible simulation and machine-learning workflows, open tools, and close collaboration with experimental researchers. We train students to formulate mechanistic questions, build reusable research infrastructure, and communicate across disciplines.</p><p>Our training and education activities connect with the <a class="text-link" href="{CPDSE_URL}">Center for Pharmaceutical Data Science Education (CPDSE)</a>.</p><a class="text-link" href="{e(data["github"])}">Explore our GitHub ↗</a></div>'

def people_content():
    profiles = ''.join(
        f'<article class="person-profile" id="{e(person["id"])}"><div><img class="person-photo" src="{e(person["photo"])}" alt="Portrait of {e(person["name"])}" loading="lazy" decoding="async"><p class="eyebrow">{e(person["role"])}</p><h2>{e(person["name"])}</h2><p>{e(person["bio"])}</p>{profile_link(person)}</div>'
        f'<div class="person-research"><h3>My research</h3><h4>{e(person["research_title"])}</h4><p>{e(person["research"])}</p><a class="text-link" href="research.html#{e(person["theme"])}">Explore the research theme →</a></div></article>'
        for person in data['people'])
    alumni = '<section class="alumni" aria-labelledby="alumni-title"><h2 id="alumni-title">Alumni</h2>' + ''.join(
        f'<article class="alumni-entry"><p class="eyebrow">{e(person["years"])}</p><div><h3>{e(person["name"])}</h3><p class="alumni-institution">{e(person["role"])} · {e(person["institution"])}</p><p>{e(person["project"])}</p></div></article>'
        for person in data.get('alumni', [])) + '</section>'
    return '<p class="lead">Meet the researchers connecting molecular mechanisms to drug discovery at MD³.</p>' + profiles + alumni

def publications_content():
    result = '<p class="lead">Publications by Icaro Ariel Simon, including work completed before the formation of MD³.</p>'
    metrics = data['bibliometrics']
    result += '<section class="bibliometrics" aria-labelledby="bibliometrics-title"><h2 id="bibliometrics-title">Bibliometrics</h2>'
    result += f'<table><caption>Summary as of {e(metrics["as_of"])}</caption><thead><tr><th scope="col">Metric</th><th scope="col">All time</th><th scope="col">{e(metrics["recent_period"])}</th></tr></thead><tbody>'
    for metric in metrics['metrics']:
        result += f'<tr><th scope="row">{e(metric["label"])}</th><td>{e(metric["value"])}</td><td>{e(metric["recent_value"])}</td></tr>'
    result += f'</tbody></table><p class="publication-note">{e(metrics["source_note"])}</p><a class="text-link" href="{e(metrics["scholar_url"])}">View Google Scholar for current metrics ↗</a></section>'
    for kind, heading in [('Peer-reviewed article', 'Peer-reviewed publications'), ('Preprint', 'Preprints')]:
        entries = [p for p in data['publications'] if p['type'] == kind]
        result += f'<section class="publication-section"><h2>{heading}</h2>'
        for p in entries:
            result += f'<article class="publication"><span class="eyebrow">{e(p["year"])} · {e(kind)}</span><h3><a href="{e(p["url"])}">{e(p["title"])}</a></h3><p>{e(p["authors"])}</p><p><em>{e(p["journal"])}</em></p>'
            if p.get('note'):
                result += f'<p class="publication-note">{e(p["note"])}</p>'
            result += f'<a class="text-link" href="{e(p["url"])}">Read {"preprint" if kind == "Preprint" else "article"} ↗</a></article>'
        if kind == 'Preprint':
            result += '<p class="publication-note">Listed as a preprint in the supplied publication list.</p>'
        result += '</section>'
    return result

def template(title, body):
    nav = ''.join(f'<a href="{p.lower()}.html" {"aria-current=\"page\"" if title == p else ""}>{p}</a>' for p in pages)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | {e(data['name'])}</title><meta name="description" content="{e(data['intro'])}">
<meta name="theme-color" content="#345b76"><meta property="og:title" content="{e(title)} | MD³ Group"><meta property="og:description" content="{e(data['intro'])}">
<link rel="icon" href="assets/md3-logo.png"><link rel="stylesheet" href="assets/style.css"><script defer src="assets/main.js"></script></head>
<body><a class="skip" href="#main">Skip to content</a><div class="institution-bar"><div class="container"><a href="{INSTITUTION_URL}">UNIVERSITY OF COPENHAGEN</a> <span><a href="{DEPARTMENT_URL}">DEPARTMENT OF DRUG DESIGN AND PHARMACOLOGY</a></span></div></div>
<header class="container header"><a class="brand" href="index.html" aria-label="MD³ Group home"><img src="assets/md3-logo.png" width="52" height="52" alt=""><span>MD<sup>3</sup> <b>GROUP</b></span></a>
<button class="menu-toggle" aria-expanded="false" aria-controls="navigation">Menu <span aria-hidden="true">☰</span></button><nav id="navigation" aria-label="Main navigation">{nav}</nav></header>
<main id="main">{body}</main><footer><div class="container footer-inner"><div><a class="footer-brand" href="index.html">MD<sup>3</sup> GROUP</a><p>{e(data['full_name'])}<br>{department_link()}<br>{institution_link()}</p></div><div class="footer-community"><a class="cpdse-logo" href="{CPDSE_URL}"><img src="assets/cpdse-logo.svg" alt="CPDSE — Center for Pharmaceutical Data Science Education" loading="lazy"></a><a class="community-link" href="{CPDSE_URL}">Pharmaceutical data science education ↗</a></div><div class="footer-links"><a href="contact.html">Contact</a><a href="{e(data['github'])}">GitHub ↗</a><span>© 2026 MD³ Group</span></div></div></footer></body></html>'''

home = f'''<section class="container hero"><div class="hero-copy"><p class="eyebrow">MECHANISMS. MOLECULES. MEDICINES.</p><h1>Understanding<br>mechanisms.<br><em>Designing discovery.</em></h1><p class="hero-description">{e(data['intro'])}</p><a class="button" href="research.html">Explore our research <span aria-hidden="true">→</span></a><a class="text-link" href="{e(data['github'])}">Our GitHub ↗</a></div><figure class="hero-art"><div class="orbit orbit-one"></div><div class="orbit orbit-two"></div><span class="art-label top-label">MOLECULAR INSIGHT</span><img src="assets/md3-logo.png" alt="MD³ cube logo with a free-energy curve" width="460" height="460"><figcaption>Mechanistic Drug Design<br>and Discovery Group</figcaption><span class="art-label bottom-label">FROM STRUCTURE TO FUNCTION</span></figure></section>
<section class="about-strip"><div class="container about-inner"><p class="eyebrow">THE MD³ GROUP</p><p>At the interface of <strong>computational chemistry, biophysics, and drug discovery.</strong> We seek to uncover molecular mechanisms and translate them into predictive strategies for designing better medicines.</p></div></section>
<section class="container section"><div class="section-heading"><div><p class="eyebrow">OUR SCIENCE</p><h2>Three perspectives.<br>One molecular understanding.</h2></div><a class="text-link" href="research.html">Discover our approach →</a></div>{cards()}</section>
<section class="container collaboration"><div><p class="eyebrow">LET’S CONNECT</p><h2>Discovery starts<br>with a conversation.</h2><p>We welcome collaborations across computational chemistry,<br class="desktop"> structural biology, pharmacology, and therapeutic discovery.</p></div>{contact()}</section>'''
(OUT / 'index.html').write_text(template('Home', home))

sections = {
 'Research': ('Our science', 'From molecular mechanisms to therapeutic discovery.', research_content()),
 'People': ('Our group', 'The people behind the science.', people_content()),
 'Publications': ('Research output', 'Our work in the literature.', publications_content()),
 'News': ('From the group', 'News & updates.', ''.join(f'<article class="publication"><span class="eyebrow">{e(n["date"])}</span><h2>{e(n["title"])}</h2><p>{e(n["text"])}</p></article>' for n in data['news']) or '<div class="notice"><h2>Watch this space</h2><p>Research highlights, group updates, and announcements will appear here.</p></div>'),
 'Join': ('Connect with MD³', 'Curious about molecular discovery?', f'<div class="prose"><p class="lead">Interested in our research? We welcome conversations with students, researchers, and potential collaborators.</p><h2>Start a conversation</h2><p>Tell us about your background, research interests, and what you would like to explore with the group.</p>{contact()}<h2>Opportunities</h2><p>Contact us to ask about current opportunities. Specific openings will be listed here when available.</p></div>'),
 'Contact': ('Get in touch', 'Let’s talk science.', f'<div class="contact-grid"><div><h2>MD³ Group</h2><p>{e(data["full_name"])}<br>{department_link()}<br>{institution_link()}<br>Denmark</p></div><div><p class="eyebrow">EMAIL</p><a class="contact-email" href="mailto:{e(data["email"])}">{e(data["email"])}</a><p class="eyebrow">CODE & RESOURCES</p><a class="text-link" href="{e(data["github"])}">github.com/mdcubed ↗</a></div></div>')
}
for title, (label, heading, content) in sections.items():
    body = f'<section class="container interior section"><p class="eyebrow">{e(label)}</p><h1>{e(heading)}</h1>{content}</section>'
    (OUT / f'{title.lower()}.html').write_text(template(title, body))
(OUT / '.nojekyll').touch()
print(f'Built {len(sections) + 1} pages in {OUT}')
