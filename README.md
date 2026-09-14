# MD³ group website

A responsive, dependency-free research group website, inspired by the navigation and academic layout of https://elgetilab.github.io/. All HTML and CSS here are newly written; no reference-site code or imagery was copied.

## Preview

The generated website is in `site/`. Open `site/index.html` directly, or run:

```sh
python3 -m http.server 8000 --directory site
```

Then visit http://localhost:8000.

## Edit

Edit `content.json` for group information, research areas, people, publications, and news. Edit `scripts/build.py` for page wording/layout, and `assets/style.css` for styling. Rebuild after changes:

```sh
python3 scripts/build.py
```

The existing entries in `content.json` provide the content schema. People have biography and “My research” fields; research themes have summaries and detailed paragraphs; publications include DOI links, article/preprint type, and optional authorship notes. News entries use `date`, `title`, and `text`.

## Content sources and editorial choices

Member biographies and research summaries were prepared from the CVs and project documents in the user-provided `website_info` folder. Roles follow the user's current instructions: Icaro Ariel Simon (PI), Pablo Baceiredo Macho (research assistant), Simon Guldbrandt Kristensen (MSc student), and Irem Demiray (MSc student). Irem's biography, LinkedIn link, and research summary use `Linkedin_Irem.pdf` and `Abstract_Irem.docx`. Alumni entries follow the user-provided names, dates, affiliations, and project descriptions. The research page summarizes the 2027–2032 research plan, with future work described as aims. Individual research sections also draw on the CPDSE project applications.

All 12 entries from `Publication_List_Icaro_Simon_small.docx` are included: 11 journal articles and one preprint. Bibliographic details and preprint classification follow that list; publication status has not been independently refreshed. The document's inconsistent headline count was not reproduced. Abbreviated author lists and the shared-first-authorship note are retained. The page identifies these as Icaro's publications, including earlier work.

Only professional biography and research summaries are included; source CVs, applications, transcripts, personal addresses, and phone numbers are not copied into the website. News remains empty pending updates.

## Branding and sources

- Group profile: https://github.com/mdcubed
- Research information: https://github.com/mdcubed/.github/blob/main/profile/README.md
- Contact email: public GitHub organization profile.
- `assets/md3-logo.png`: downloaded from the group's public GitHub avatar; it matches the supplied cube branding. Replace with a higher-resolution original if desired.
- Institution and department: supplied branding.

## Publish on GitHub Pages

Create a repository named `mdcubed.github.io` under the `mdcubed` organization and push this project to its `main` branch. In the repository's **Settings → Pages**, choose **GitHub Actions** as the source. The included workflow builds and deploys `site/`. The expected address is https://mdcubed.github.io/.

This project has not been pushed or published. Publishing requires access to the organization. It also works as a project site because internal asset and page links are relative.

## Profile photos and bibliometrics

Profile photos are stored in `assets/people/` and referenced by each person's `photo` field. They are displayed at their original aspect ratio.

The publications summary is editable under `bibliometrics` in `content.json`. Values come from `Icaro_Google_Scholar_Sept_2026.pdf`: all-time citations 598, h-index 7, i10-index 7; since 2021 citations 583, h-index 7, i10-index 6. The snapshot is dated September 2026. Update the values and `as_of` together when refreshing them. The page links to the PI’s Google Scholar profile for current metrics.

## Institutional links

The header, footer, and contact details link to the University of Copenhagen (https://www.ku.dk/en) and Department of Drug Design and Pharmacology (https://drug.ku.dk/). The research training section and shared footer link to CPDSE (https://cpdse.dk/).

`assets/cpdse-logo.svg` is the unmodified official wide gold logo downloaded from https://cpdse.dk/assets/logo_wide_gold.svg. It is displayed in a linked footer panel on all pages.

Research and project descriptions use receptor-family names and generic photoswitchable ligand platform wording. Published article titles remain verbatim for bibliographic accuracy. University names within biographies and alumni entries are plain text.
