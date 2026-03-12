# Plan: Bilingual Site (RU/EN) with Translated Posts via Claude Haiku 4.5

## Overview

Set up MagicDPD as a bilingual Hugo site (Russian + English), with both languages served
under explicit prefixes (`/ru/` and `/en/`). Translated posts use Hugo's filename-suffix
convention (`post.en.md` alongside `post.md` in the same directory), so Hugo automatically
links them as translations and the Anubis theme can render the language switcher.

**Scope:**
1. Update translation script to write `.en.md` files into `site/content/posts/`
2. Configure Hugo for bilingual mode (`[languages]` block, `defaultContentLanguageInSubdir`)
3. Enable language switcher in site header (Anubis already has the partial)
4. Translate static pages: About and Archive
5. Translate all 3134 posts iteratively by year-batch
6. Validate full Hugo build

Translation uses `claude -p` subprocess (Claude Code subscription auth, no API key).
Resume-safe: progress tracked in `scripts/translate_progress.json`.

## Validation Commands

- `python3 -m py_compile scripts/translate_posts.py`
- `python3 -c "import frontmatter; print('deps ok')"`
- `hugo --source site version`

---

### Task 1: Verify dependencies

- [x] `python-frontmatter` already in `requirements.txt` — no new packages needed
- [x] Verify: `source .venv/bin/activate && python3 -c "import frontmatter; print('ok')"`
- [x] Mark completed

---

### Task 2: Create translation script `scripts/translate_posts.py`

Script uses `claude -p` subprocess (Claude Code subscription auth, no API key needed).

- [ ] Create `scripts/translate_posts.py` — implemented with:
  - `translate_text(text)` — calls `subprocess.run(["claude", "-p", prompt, "--model", MODEL])`
  - Detects `"You've hit your limit"` in output → raises `RateLimitError`
  - `load_progress()` / `save_progress()` — JSON resume tracker
  - `translate_post(md_path)` — parses front matter, translates `title` + body, writes to `OUTPUT_DIR`
  - `main()` — `--limit N` and `--year YYYY` CLI args, per-file error handling
- [ ] Verify syntax: `python3 -m py_compile scripts/translate_posts.py`
- [ ] Mark completed

---

### Task 3: Update translation script output format to `.en.md` suffix

Hugo's multilingual filename-suffix convention requires English posts to live in the same
directory as Russian originals, named `<slug>.en.md`. Update the script accordingly.

- [ ] In `scripts/translate_posts.py`, change the two output constants:
  ```python
  POSTS_DIR = Path("site/content/posts")
  OUTPUT_DIR = Path("site/content/posts")   # same dir as source
  ```
- [ ] In `translate_post()`, change the output filename from `md_path.name` to
  `md_path.stem + ".en.md"` so that `2015-07-03-slug.md` → `2015-07-03-slug.en.md`
- [ ] Also add `post.metadata["language"] = "en"` is NOT needed — Hugo detects language
  from the filename suffix automatically; do not add it
- [ ] Remove the empty `site/content/posts-en/` directory:
  `rm -rf site/content/posts-en`
- [ ] Verify syntax: `python3 -m py_compile scripts/translate_posts.py`
- [ ] Mark completed

---

### Task 4: Configure Hugo for bilingual mode in `site/hugo.toml`

Enable both languages under explicit URL prefixes (`/ru/` and `/en/`).

- [ ] Add `defaultContentLanguageInSubdir = true` on the line after `defaultContentLanguage = "ru"`
- [ ] Remove the top-level `[menu]` block (it will be replaced per-language below)
- [ ] Remove the top-level `[params]` fields `author` and `description` (moved per-language)
- [ ] Add the following `[languages]` block at the end of `site/hugo.toml`:

  ```toml
  [languages]

    [languages.ru]
      languageName = "Русский"
      weight = 1
      title = "MagicDPD: Magic Driven Product Development!"

      [languages.ru.params]
        author = "GlukRazor"
        description = "Архив постов MagicDPD"

      [[languages.ru.menu.main]]
        identifier = "home"
        name = "Главная"
        title = "Главная"
        url = "/"
        weight = 1

      [[languages.ru.menu.main]]
        identifier = "archive"
        name = "Архив"
        title = "Архив постов"
        url = "/archive/"
        weight = 2

      [[languages.ru.menu.main]]
        identifier = "about"
        name = "О проекте"
        title = "О проекте"
        url = "/about/"
        weight = 3

    [languages.en]
      languageName = "English"
      weight = 2
      title = "MagicDPD: Magic Driven Product Development!"

      [languages.en.params]
        author = "GlukRazor"
        description = "MagicDPD post archive — CAE/FEA/CFD simulation engineering"

      [[languages.en.menu.main]]
        identifier = "home"
        name = "Home"
        title = "Home"
        url = "/"
        weight = 1

      [[languages.en.menu.main]]
        identifier = "archive"
        name = "Archive"
        title = "Post archive"
        url = "/archive/"
        weight = 2

      [[languages.en.menu.main]]
        identifier = "about"
        name = "About"
        title = "About the project"
        url = "/about/"
        weight = 3
  ```

- [ ] Verify Hugo parses the config without errors:
  `hugo --source site config | grep -E "defaultContent|languages"`
- [ ] Mark completed

---

### Task 5: Enable language switcher in site header

The Anubis theme already has `language-switcher.html` partial but does not include it in
the header by default. Override `header-extra.html` to activate it.

- [ ] Create `site/layouts/partials/header-extra.html` with the following content:
  ```html
  {{ partial "language-switcher.html" . }}
  ```
  (This overrides the theme's empty `<!--for overriding-->` placeholder.)
- [ ] Verify the file exists: `cat site/layouts/partials/header-extra.html`
- [ ] Mark completed

---

### Task 6: Translate static pages (About and Archive)

Create English versions of the two non-post content pages using `claude -p`.

- [ ] Translate `site/content/about/_index.md` body and title:
  run `claude -p` with the translation system prompt and the file content,
  save result as `site/content/about/_index.en.md` with translated `title` front matter
  and English body
- [ ] Create `site/content/archive/_index.en.md` with front matter:
  ```yaml
  ---
  title: "Post Archive"
  ---
  ```
  (Archive is auto-generated by Hugo; only the title needs translation)
- [ ] Verify both files exist:
  `ls site/content/about/_index.en.md site/content/archive/_index.en.md`
- [ ] Mark completed

---

### Task 7: Smoke-test translation on 5 recent posts

Verify the updated script works end-to-end with the new `.en.md` output format.

- [ ] Run: `source .venv/bin/activate && python3 scripts/translate_posts.py --year 2025 --limit 5`
- [ ] Verify output files exist as `.en.md` in the posts directory:
  `ls site/content/posts/*.en.md | head -5`
- [ ] Inspect one output file and confirm:
  - Filename ends in `.en.md`
  - Front matter intact (layout, date, author, source, images unchanged)
  - `title` is translated to English
  - Body is translated to English
  - URLs and code blocks unchanged
- [ ] Do a quick Hugo build to confirm no errors so far:
  `hugo --source site --buildDrafts 2>&1 | tail -5`
- [ ] Mark completed

---

### Task 8: Translate posts from 2015 and 2016

First full year-batch — ~400 oldest posts.

- [ ] Run: `source .venv/bin/activate && python3 scripts/translate_posts.py --year 2015 --year 2016`
- [ ] Verify count: `ls site/content/posts/2015-*.en.md site/content/posts/2016-*.en.md | wc -l`
- [ ] Check progress: `python3 -c "import json; d=json.load(open('scripts/translate_progress.json')); print(len(d), 'done')"`
- [ ] Mark completed

---

### Task 9: Translate posts from 2017, 2018, and 2019

- [ ] Run: `source .venv/bin/activate && python3 scripts/translate_posts.py --year 2017 --year 2018 --year 2019`
- [ ] Verify: `ls site/content/posts/201[789]-*.en.md | wc -l`
- [ ] Mark completed

---

### Task 10: Translate posts from 2020, 2021, and 2022

- [ ] Run: `source .venv/bin/activate && python3 scripts/translate_posts.py --year 2020 --year 2021 --year 2022`
- [ ] Verify: `ls site/content/posts/202[012]-*.en.md | wc -l`
- [ ] Mark completed

---

### Task 11: Translate posts from 2023, 2024, and 2025

- [ ] Run: `source .venv/bin/activate && python3 scripts/translate_posts.py --year 2023 --year 2024 --year 2025`
- [ ] Verify: `ls site/content/posts/202[345]-*.en.md | wc -l`
- [ ] Mark completed

---

### Task 12: Validate full translation coverage and Hugo build

- [ ] Run coverage check:
  ```bash
  python3 -c "
  from pathlib import Path
  src = set(p.stem for p in Path('site/content/posts').glob('[0-9]*.md'))
  out = set(p.stem.removesuffix('.en') for p in Path('site/content/posts').glob('*.en.md'))
  missing = src - out
  print(f'Total: {len(src)}, Translated: {len(out)}, Missing: {len(missing)}')
  for f in sorted(missing)[:20]:
      print(' MISSING:', f)
  "
  ```
- [ ] If missing files exist, re-run without year filter:
  `source .venv/bin/activate && python3 scripts/translate_posts.py`
  (already-translated files skipped via progress tracker)
- [ ] Run full Hugo build and confirm no errors:
  `hugo --source site 2>&1 | tail -10`
- [ ] Confirm both language roots exist in output:
  `ls site/public/ru/ && ls site/public/en/`
- [ ] Final translation count must show `Missing: 0`
- [ ] Mark completed
