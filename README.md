# Fan Yang · Personal Website

Personal academic and professional website for **Fan Yang (杨帆)**, a system architect at Huawei Cloud and a Tsinghua University Ph.D.

The site retains the original repository's white background, compact profile header, section navigation, and year-grouped publication layout.

## Repository and address

- Repository: https://github.com/CSyyyang/yfrank.github.io
- GitHub Pages address for this repository: https://csyyyang.github.io/yfrank.github.io/
- Publishing source: `master`, repository root `/`.

The repository is a **project site**: its owner is `CSyyyang`, so the repository name alone does not give it the `yfrank.github.io` domain. Enable Pages in repository **Settings → Pages → Deploy from a branch → master → /(root)**. The address above becomes available after a successful Pages deployment.

## Edit and build

| File | Purpose |
| --- | --- |
| `js_index.html` | Editable page: profile, work, education, honors, and SEO metadata |
| `papers/publications.json` | Publication records, authors, years, and verified paper links |
| `script.js` | Renders publication groups and highlights Fan Yang, including co-first authorship |
| `style.css` | Responsive layout and styling |
| `assets/yf.jpg` | Profile photo already present in the repository |
| `render.py` | Runs the shared JavaScript renderer using Node.js and generates the static page |
| `index.html` | Generated page served by GitHub Pages; all publications work without JavaScript |
| `robots.txt`, `sitemap.xml` | Search engine discovery with the correct project-site URL |

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
