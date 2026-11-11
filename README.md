# TSA at the University of Michigan

Five static pages in the **Michigan After Hours** style: Michigan blue `#00274C`, deep crimson `#B5121B`, and white.

- `index.html` — Home
- `board.html` — Board (all nine supplied members, alphabetically by last name)
- `events.html` — Upcoming gatherings and past-event photo albums
- `newsletter.html` — The TSA Weekly, issue reader, archive, and email signup requests
- `join.html` — Joining inquiries, collaboration, and contact

## Edit content

Edit `data/site.json`, then run:

```sh
python scripts/build.py
```

Commit the data file **and** the generated HTML pages. The generated pages serve directly on GitHub Pages, without a JavaScript build, package installation, or external dependencies. Do not manually edit generated HTML for lasting content changes; rebuilds replace it. Layout and copy live in `scripts/build.py`; styling in `assets/styles.css`; interactions in `assets/site.js`.

### Board portraits and bios

Add images under `assets/images/board/` and set each member's `photo` to a relative path, for example `assets/images/board/arda-edil.jpg`. Set `bio` to the member's short introduction. Empty photos show an initials placeholder; empty bios are omitted. Names, roles, and emails match the user's supplied list; spellings can be updated in the data file.

### Events and albums

Replace the sample event entries. Each entry has `id`, `title`, `date`, `location`, `upcoming`, `sample`, `summary`, `cover`, and `photos`. Set `sample` to `false` for confirmed entries. A cover is a local image path or HTTPS URL. Add album photos as objects:

```json
{"src": "assets/images/events/picnic-01.jpg", "alt": "TSA members gathering at the welcome picnic"}
```

Missing covers and empty albums deliberately show placeholders. Sample listings are clearly marked; they are not real announcements. Supply confirmed dates and venues before treating events as published.

The current albums use official photos supplied in the TSA Google Drive folder: the Vic South rooftop mangal, November 1 Republic Day brunch, November 7 tailgate/game day, and a soccer photo collection. Mangal is labeled as the first weekend of the semester; no exact date was supplied. The soccer collection has a semester label rather than a single event date.

Optimized WebP copies are stored in `assets/images/events/`. Their source filenames and dimensions are recorded in `data/photo-sources.json`; the original files remain unchanged in Drive. Three near-duplicate scoreboard frames, two campus-table photos awaiting event context, and the video were not published in this pass. Board portraits remain placeholders because none of these files are labeled as individual portraits.

`heroPhoto` and `heroPhotoAlt` control the homepage group photograph. `homeFeaturedEvent` selects the event featured farther down the homepage. Event `titleTr` values add Turkish subtitles.

### Newsletters

The first newsletter in the list is featured. Each entry has `id`, `title`, `date`, `sample`, `summary`, and a `paragraphs` array of plain-text paragraphs. Replace the sample issues and set `sample` to `false`. The sample notice disappears when all editions are real.

### Contact and subscriptions

The current contact is **Arda Edil (President), ardaedil@umich.edu**, taken from the supplied authorized list. Change `contactEmail` and `contactName` if TSA should use a shared inbox. Set optional `instagramUrl` or `communityUrl` when confirmed; absent links are omitted.

This site has no email backend or mailing-list provider. Contact and newsletter-request forms create a **mailto draft** in the visitor's email app. Visitors must send the draft themselves; no message delivery or subscription is claimed. Both forms have direct email fallbacks. Connect a service later if automatic submissions or subscriptions are desired.

## Preview locally

```sh
python -m http.server 4173 --bind 127.0.0.1
```

Open `http://127.0.0.1:4173/`. The site uses relative links and also supports a GitHub Pages repository subpath such as `/tsa-website/`.

Check generated links, asset paths, form labels, page headings, issue data, and the nine-member roster with `python scripts/check.py`. JavaScript syntax can be checked with `node --check assets/site.js`.

## GitHub Pages

Live preview: [ardaedil.github.io/tsa-website](https://ardaedil.github.io/tsa-website/).

GitHub Pages publishes the generated HTML and assets from **main → /(root)**. Changes pushed to `main` trigger the Pages deployment. `.nojekyll` prevents extra processing. The U-M website is hosted separately and is not changed by GitHub Pages deployments.

Navigation links remain visible on every screen size. English page titles are paired with selected Turkish labels, marked with `lang="tr"` for assistive technologies.

## Original website backup

The complete original site, including its photographs, fonts, scripts, and HTML, is preserved on:

[`codex/backup-legacy-2026-11-10`](https://github.com/ardaedil/tsa-website/tree/codex/backup-legacy-2026-11-10)

Backup commit: `ff04d672417c62a6422afe48ba7837ce2924e970`.

The original `constitution.pdf` is also retained in the current site. To inspect the old version locally, use a separate checkout or switch to the backup branch after saving current work. The backup branch should remain unchanged.
