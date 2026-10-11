# AGENTS.md

This file provides guidance to coding agents when working with code in this repository.

## Project Overview

Personal academic and professional website for Fan Yang (杨帆), hosted at `https://yfrank1.github.io/` using GitHub Pages. The site uses a hybrid static/dynamic rendering approach: `js_index.html` is the editable source template, and `index.html` is the pre-rendered static output served to users.

## Build

**Prerequisites**: Python 3.9+ and Node.js 18+. No third-party packages or browser downloads are required.

**Build command:**
```bash
python render.py
```

**Read-only validation:** `python render.py --check` checks publication data and compares the generated homepage with `index.html` without writing files. It deliberately ignores sitemap dates. Run `python -m unittest discover -s tests` for build validation and failure-protection tests, and `node --test tests/publications.test.js` for publication resource links and escaping. GitHub Actions runs these checks on pushes and pull requests.

Note: use `python` (not `python3`) on Windows. No local HTTP server is required to build.

The build script executes the shared `renderPublications` function from `script.js` using Node.js, inserts the generated publication HTML into `js_index.html`, checks the publication count, writes `index.html`, and updates `sitemap.xml`. The dynamic page and static build use the same renderer. A rendering failure must not overwrite the previous output.

**Local development preview:**
```bash
python -m http.server 8000 --bind 0.0.0.0
# Then open http://localhost:8000/js_index.html
```

Use `js_index.html` for live development (dynamic JS), then run the build to regenerate `index.html` for production.

## Architecture

### Two-file rendering pattern
- **`js_index.html`** — the source of truth for page structure and content; loads `script.js` to dynamically render publications
- **`index.html`** — auto-generated static output; do not edit directly
- **`script.js`** — shared escaped-HTML publication renderer, usable in a browser or with Node.js. The browser loads `papers/publications.json`; the build reads the same file locally. The runtime script is stripped from the output during build.

### Content data
- **`papers/publications.json`** — single source of truth for all publications. Each entry has: `title`, `authors` (array), `venue`, `short`, `year` (integer), `link`, and optional `pdf`, `code`, `award`, `note`, and `equalContribution` fields. Publications are grouped by year (descending). Fan Yang is bold/highlighted automatically, including starred author names; first and co-first authored papers appear first within each year.
- `year` must be an integer (not a string), or `null` when the publication year is not provided. Records with `year: null` appear under Accepted / Forthcoming; `venue` may also be `null` when not provided. `link` and `code` should be a URL string or `null`; omitting them is also acceptable.
- Awards shorter than 30 characters are displayed inline after the venue; longer awards appear on a new line below.
- Keep editorial details (fast-track invitations and acceptance notes) in `note`, separate from `award`. Preserve confirmed publication facts; do not infer acceptance status from a future conference year.
- Papers with no `link` render the title as plain text (no `<a>` tag); do not use `"link": ""` as a substitute for no link — use `null` or omit the field.
- Linked papers have explicit Paper, DOI, or PDF resource links. Avoid duplicate PDF resource links when `link` and `pdf` point to the same file. CCF labels link to `ccfSource` when provided; omit unsupported ratings rather than inferring a category from conference sponsorship.

### Styling
- **`style.css`** — single custom stylesheet, no CSS frameworks or external dependencies. Responsive via media queries at 567px, 768px, and 1200px.
- CSS class for blue-colored links/tags is `.blue-tag` (not `.bule-tag`).
- Keep `assets/yf-white.png` as the original portrait. The page uses `yf-portrait-288.webp` and `yf-portrait-432.webp` through `srcset`; do not restore the full-resolution original as the page image or favicon.
- The architecture figure uses a readable vertical SVG below 568px, while the original desktop diagram remains available at full size. Keep the content and responsibility boundary consistent between both diagrams.
- `assets/social-card.svg` is the editable source for the 1200×630 PNG referenced by Open Graph and Twitter metadata. Re-export the PNG when the card source changes.

### SEO metadata
`js_index.html` contains JSON-LD schema.org markup, Open Graph tags, and Twitter Card tags. The sitemap (`sitemap.xml`) is auto-updated with each build. After building, submit the sitemap to Google Search Console and Bing Webmaster Tools if significant content was added.

## Key workflow

To update publications: edit `papers/publications.json`, then run `bash build.sh` to regenerate `index.html`.

To update page content (bio, research section, links, etc.): edit `js_index.html`, then run `bash build.sh`.

Never manually edit `index.html` — it is overwritten on every build.

CCF labels use `ccfLabel` and `ccfSource` in publications.json. International ratings use the 2026 seventh edition (not publication-year ratings); CRAD uses the separate 2019 Chinese-journal A category. The user confirmed Tape in the Cloud's venue as ACM Transactions on Storage (2026), rated CCF-A.
