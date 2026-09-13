# Fan Yang · Personal Website

Personal academic and professional website for **Fan Yang (杨帆)**, a system architect at Huawei Cloud and a Tsinghua University Ph.D.

The site retains the original repository's white background, compact profile header, section navigation, and year-grouped publication layout.

## Repository and address

- Repository: https://github.com/yfrank1/yfrank1.github.io
- GitHub Pages address for this repository: https://yfrank1.github.io/
- Publishing source: `master`, repository root `/`.

The repository is a **personal site**: its name `yfrank1.github.io` matches the owner `yfrank1`, so it is served at the root address above. Enable Pages in repository **Settings → Pages → Deploy from a branch → master → /(root)**. The address above becomes available after a successful Pages deployment.

## Edit and build

| File | Purpose |
| --- | --- |
| `js_index.html` | Editable page: profile, work, education, honors, and SEO metadata |
| `papers/publications.json` | Publication records, authors, years, and verified paper links |
| `script.js` | Renders publication groups and highlights Fan Yang, including co-first authorship |
| `style.css` | Responsive layout and styling |
| `assets/yf-white.png` | White-background portrait, displayed without cropping |
| `render.py` | Runs the shared JavaScript renderer using Node.js and generates the static page |
| `index.html` | Generated page served by GitHub Pages; all publications work without JavaScript |
| `robots.txt`, `sitemap.xml` | Search engine discovery with the correct personal-site URL |

Build requirements: Python 3.9+ and Node.js 18+. No package installation or browser download is needed.

```bash
python render.py
```

On macOS/Linux, `bash build.sh` is also supported. No HTTP server is required to build.
Commit the updated source files **and generated `index.html` / `sitemap.xml`**. Do not edit `index.html` by hand.
The deployed site has no runtime dependency on Python, Node.js, or a backend service.

## Content provenance

- The Tsinghua profile provides the profile identity, doctoral advisors, and the main publication list: https://storage.cs.tsinghua.edu.cn/~yf/
- The supplied CV provides education dates, undergraduate rank, and seven honors from 2014–2022.
- The supplied work summary provides current responsibilities. The public page describes the technical scope without reproducing internal product roadmaps, customer data, or unpublished commercial measurements.
- The FAST 2026 proceedings confirm TapeOBS and equal contribution by Qing Wang and Fan Yang: https://www.usenix.org/system/files/fast26-wang.pdf
- Aria is ICDE **2021**; the supplied CV's 2020 date and author order are corrected using the paper: https://storage.cs.tsinghua.edu.cn/papers/icde21-aria.pdf
- The APPT paper is **2019**: https://doi.org/10.1007/978-3-030-29611-7_4
- The ACM MM paper's title is **InvisibleFL**, with the author list corroborated by the first author's publication page: https://liqiushi.fyi/papers.html
- Hera (MICRO 2026) is listed on the Tsinghua profile. A paper URL is not fabricated when the source provides none; the title is rendered as plain text.

The former template owner's biography, publications, awards, email, Scholar identifier, metadata, and analytics account have been removed from the served page. The uploaded full CV and work summary are not included in this public repository.

## Google Scholar reconciliation (2026-09-13)

The supplied two-page Scholar PDF contains 11 rows. Ten complete titles are already represented in publications.json. The truncated row “in Full-Path-Indexed File System” appears to duplicate the APPT 2019 paper, with an incomplete author list; it is not added as a separate paper pending contrary evidence. Hera (MICRO 2026), present on the Tsinghua profile but absent from this Scholar snapshot, is retained. The website therefore lists 11 distinct papers.

The snapshot supplies page ranges added to seven records. The PACT 2022 DOI is 10.1145/3559009.3569676. The survey DOI and PDF were verified against the journal publication at https://crad.ict.ac.cn/cn/article/pdf/preview/10.7544/issn1000-1239.2020.20190820.pdf . Full author names remain sourced from the existing primary references, rather than malformed or abbreviated Scholar author strings.
