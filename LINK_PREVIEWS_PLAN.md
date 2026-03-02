# План реализации статических превью через GitHub Actions

## Общая схема

```
CI: Python fetch_link_previews.py → enriched front matter → hugo build → статический HTML
```

Никакого JS, никаких API-запросов в runtime. Всё готово при сборке.

---

## Шаг 1 — Новый скрипт `fetch_link_previews.py`

Создать в корне репозитория. Задача: обходит все `.md` файлы в `site/content/posts/`, извлекает URL из текста regex'ом, делает `link_preview()` для каждого, дописывает результат в front matter.

**Входные данные** (существующий front matter поста):
```yaml
---
title: "PZFlex solver"
date: 2026-02-03
---
https://www.wikiwand.com/en/articles/PZFlex
https://www.youtube.com/@PZFlex
```

**Результат** (обогащённый front matter):
```yaml
---
title: "PZFlex solver"
date: 2026-02-03
link_previews:
  - url: "https://www.wikiwand.com/en/articles/PZFlex"
    title: "PZFlex - Wikiwand"
    description: "Specialized FEA acoustic solver..."
    image: "https://..."
  - url: "https://www.youtube.com/@PZFlex"
    title: "PZFlex - YouTube"
    description: ""
    image: "https://i.ytimg.com/..."
---
```

**Детали реализации**:
- Парсить front matter через `python-frontmatter` (или вручную через `---` разделитель)
- URL regex: `https?://[^\s\)\]>]+`
- Пропускать уже обработанные URL (кэш в `link_previews_cache.json`) — чтобы при каждом билде не перефетчивать всё заново
- Timeout на запрос: ~5 сек, при ошибке — пропустить URL
- Добавить в `requirements.txt`: `linkpreview`, `python-frontmatter`

---

## Шаг 2 — Новый Hugo partial `link-preview-card.html`

Создать `site/layouts/partials/link-preview-card.html` — статический рендер карточки из front matter данных:

```html
{{ with .preview }}
<a class="link-preview__card" href="{{ .url }}" target="_blank" rel="noopener">
  {{ with .image }}
  <span class="link-preview__thumb-wrap">
    <img class="link-preview__thumb" src="{{ . }}" loading="lazy">
  </span>
  {{ end }}
  <span class="link-preview__body">
    <span class="link-preview__title">{{ .title }}</span>
    {{ with .description }}
    <span class="link-preview__description">{{ . }}</span>
    {{ end }}
    <span class="link-preview__host">{{ .url | urls.Parse | .Host }}</span>
  </span>
</a>
{{ end }}
```

CSS уже есть в `site/assets/css/link-previews.css` — классы совпадают, ничего нового писать не нужно.

---

## Шаг 3 — Обновить `single.html` темы

Создать `site/layouts/_default/single.html` (override темы anubis), добавить рендер превью из front matter после контента:

```html
{{ define "main" }}
    <article class="post h-entry">
        ...
        <div class="content e-content">
            {{ .Content }}
        </div>
        {{ with .Params.link_previews }}
        <div class="post-link-previews">
            {{ range . }}
            {{ partial "link-preview-card.html" (dict "preview" .) }}
            {{ end }}
        </div>
        {{ end }}
        {{ partial "post-info.html" . }}
    </article>
{{ end }}
```

---

## Шаг 4 — Обновить `post-summary.html`

Уже переопределён в `site/layouts/partials/post-summary.html`. Показывать первое превью из `link_previews`:

```go
{{- with .Params.link_previews -}}
    {{ partial "link-preview-card.html" (dict "preview" (index . 0)) }}
{{- end -}}
```

Убрать текущую логику с `Params.links` и JS-зависимостью.

---

## Шаг 5 — Отключить JS-превью в `hugo.toml`

```toml
[params.linkPreviews]
  enabled = false  # теперь всё статично
```

`render-link.html` перестанет генерировать JS-зависимые `<span>`.

---

## Шаг 6 — Обновить GitHub Actions CI

```yaml
# .github/workflows/jekyll.yml

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Cache link previews
        uses: actions/cache@v4
        with:
          path: link_previews_cache.json
          key: link-previews-${{ hashFiles('site/content/posts/**') }}

      - name: Install Python deps
        run: pip install linkpreview python-frontmatter requests beautifulsoup4 lxml

      - name: Fetch link previews
        run: python fetch_link_previews.py

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: "0.157.0"
          extended: true

      - name: Build with Hugo
        run: hugo --minify
        working-directory: site

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: site/public
```

**Ключевой момент**: кэш `link_previews_cache.json` сохраняется между запусками CI. При добавлении нового поста — фетчатся только новые URL, старые берутся из кэша. Это экономит время сборки и избегает повторных запросов.

---

## Порядок реализации

| # | Задача | Файлы |
|---|---|---|
| 1 | Написать `fetch_link_previews.py` | новый файл |
| 2 | Добавить `linkpreview`, `python-frontmatter` в `requirements.txt` | `requirements.txt` |
| 3 | Создать `link-preview-card.html` | `site/layouts/partials/` |
| 4 | Обновить `single.html` | `site/layouts/_default/` |
| 5 | Обновить `post-summary.html` | `site/layouts/partials/` |
| 6 | Отключить JS-превью в `hugo.toml` | `site/hugo.toml` |
| 7 | Обновить CI workflow | `.github/workflows/jekyll.yml` |
