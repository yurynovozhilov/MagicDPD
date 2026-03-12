# Plan: Translate Blog Posts to Technical English via Claude Haiku 4.5

## Overview

Translate all 3134 Russian-language Markdown posts in `site/content/posts/` to technical
English using the Claude Haiku 4.5 model (`claude-haiku-4-5-20251001`). Each post has YAML
front matter and a Markdown body. The script iterates over every `.md` file, translates the
`title` field and body text, and saves the English version to `site/content/posts-en/`
preserving all structural front matter fields unchanged.

Translation rules:
- Translate `title` front matter field and body text from Russian to technical English
- Preserve unchanged: `layout`, `date`, `author`, `source`, `images`, `tags`, `url` fields
- Preserve unchanged in body: URLs, code blocks (fenced and inline), Markdown syntax,
  product/company names (ANSYS, LS-DYNA, COMSOL, Abaqus, OpenFOAM, etc.), emoji
- Resume-safe: skip already-translated files using a JSON progress tracker
- Rate-limit-safe: respect API limits with exponential backoff on 429 errors

## Validation Commands

- `python3 -m py_compile scripts/translate_posts.py`
- `python3 -c "import anthropic, frontmatter; print('deps ok')"`
- `test -d site/content/posts-en && echo "output dir ok"`

---

### Task 1: Add Anthropic SDK to project dependencies

- [ ] Add `anthropic>=0.40.0` to `requirements.txt` under a new `# Translation` comment
- [ ] Activate the virtual environment and install the new dependency:
  `source .venv/bin/activate && pip install anthropic`
- [ ] Verify install: `python3 -c "import anthropic; print(anthropic.__version__)"`
- [ ] Mark completed

---

### Task 2: Create translation script `scripts/translate_posts.py`

Implement the full translation pipeline as a single self-contained script.

- [ ] Create `scripts/translate_posts.py` with the following structure:

  **Constants / config (at top of file):**
  ```python
  POSTS_DIR = Path("site/content/posts")
  OUTPUT_DIR = Path("site/content/posts-en")
  PROGRESS_FILE = Path("scripts/translate_progress.json")
  MODEL = "claude-haiku-4-5-20251001"
  MAX_TOKENS = 4096
  ```

  **`load_progress() -> set[str]`** — reads `PROGRESS_FILE` and returns a set of
  already-translated filenames; returns empty set if file not found.

  **`save_progress(done: set[str])`** — atomically writes the set to `PROGRESS_FILE`
  as a sorted JSON list.

  **`translate_text(client, text: str) -> str`** — sends `text` to Claude Haiku 4.5
  with a system prompt instructing it to translate Russian technical CAE/FEA content to
  technical English. The system prompt must specify:
  - Output only the translated text, no commentary
  - Preserve all Markdown syntax, URLs, code blocks verbatim
  - Preserve product/company names: ANSYS, LS-DYNA, COMSOL, Abaqus, OpenFOAM,
    SolidWorks, Altair, HyperMesh, Nastran, RADIOSS, STAR-CCM+, SimScale, etc.
  - Preserve emoji characters
  - This is a technical CAE/simulation engineering blog — use accurate technical terms

  **`translate_post(client, md_path: Path) -> None`** — loads a post with
  `frontmatter.load()`, translates `post.metadata['title']` and `post.content` via
  `translate_text()`, constructs the output path under `OUTPUT_DIR` with the same
  filename, writes the result with `frontmatter.dump()`.

  **`main()`** — loads progress, iterates sorted over all `.md` files in `POSTS_DIR`,
  skips already-done files, calls `translate_post()`, saves progress after each file,
  prints a one-line status per post: `[N/3134] filename.md`. Handle `anthropic.RateLimitError`
  with `time.sleep(60)` and retry once. Handle all other exceptions by printing the error
  and continuing to the next file (do not abort the full run).

- [ ] Ensure `OUTPUT_DIR` is created at startup with `OUTPUT_DIR.mkdir(parents=True, exist_ok=True)`
- [ ] Use `python-dotenv` to load `.env` for `ANTHROPIC_API_KEY`
- [ ] Verify syntax: `python3 -m py_compile scripts/translate_posts.py`
- [ ] Mark completed

---

### Task 3: Smoke-test translation on 5 recent posts

Run a limited test to verify the script works end-to-end before committing to the full run.

- [ ] Run the script limited to the 5 newest posts (2025 year posts) by temporarily adding
  a `--limit 5` CLI argument (use `argparse`) that stops after N translations
- [ ] Execute: `source .venv/bin/activate && python3 scripts/translate_posts.py --limit 5`
- [ ] Inspect 2 output files in `site/content/posts-en/` and confirm:
  - Front matter is intact (layout, date, author, source, images unchanged)
  - Title is translated to English
  - Body text is translated to English
  - URLs and code blocks are unchanged
- [ ] Mark completed

---

### Task 4: Translate posts from 2015 and 2016

First full year-batch — ~400 oldest posts.

- [ ] Run: `source .venv/bin/activate && python3 scripts/translate_posts.py --year 2015 --year 2016`
- [ ] Add `--year` argument to `main()` using `argparse` that filters posts by filename prefix
  (e.g. `--year 2015` processes only files starting with `2015-`); multiple `--year` flags
  are OR-combined
- [ ] After run completes, verify count:
  `ls site/content/posts-en/2015-* site/content/posts-en/2016-* | wc -l`
- [ ] Check progress file updated: `python3 -c "import json; d=json.load(open('scripts/translate_progress.json')); print(len(d), 'done')"`
- [ ] Mark completed

---

### Task 5: Translate posts from 2017, 2018, and 2019

- [ ] Run: `source .venv/bin/activate && python3 scripts/translate_posts.py --year 2017 --year 2018 --year 2019`
- [ ] After run completes, verify: `ls site/content/posts-en/201[789]-* | wc -l`
- [ ] Mark completed

---

### Task 6: Translate posts from 2020, 2021, and 2022

- [ ] Run: `source .venv/bin/activate && python3 scripts/translate_posts.py --year 2020 --year 2021 --year 2022`
- [ ] After run completes, verify: `ls site/content/posts-en/202[012]-* | wc -l`
- [ ] Mark completed

---

### Task 7: Translate posts from 2023, 2024, and 2025

- [ ] Run: `source .venv/bin/activate && python3 scripts/translate_posts.py --year 2023 --year 2024 --year 2025`
- [ ] After run completes, verify: `ls site/content/posts-en/202[345]-* | wc -l`
- [ ] Mark completed

---

### Task 8: Validate full translation coverage

- [ ] Run coverage check:
  ```bash
  python3 -c "
  from pathlib import Path
  src = set(p.name for p in Path('site/content/posts').glob('*.md'))
  out = set(p.name for p in Path('site/content/posts-en').glob('*.md'))
  missing = src - out
  print(f'Total: {len(src)}, Translated: {len(out)}, Missing: {len(missing)}')
  if missing:
      for f in sorted(missing)[:20]:
          print(' MISSING:', f)
  "
  ```
- [ ] If missing files exist, re-run the script without `--year` filter to catch stragglers:
  `source .venv/bin/activate && python3 scripts/translate_posts.py`
  (already-translated files will be skipped via progress tracker)
- [ ] Final count must show `Missing: 0`
- [ ] Mark completed
