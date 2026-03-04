#!/usr/bin/env python3
"""
For VK posts where the title was auto-generated from the first 60 chars of
the first line (and the line was NOT removed from the body), this script:
  1. Extracts the first sentence from the body as the new title
  2. Removes that sentence from the body

Detection: body's first text line starts with the current title text
           → indicates the title was auto-generated (not explicit).

Uses only stdlib.
"""
import re
from pathlib import Path

SITE_POSTS = Path("site/content/posts")

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)", re.DOTALL)
TITLE_LINE_RE   = re.compile(r"^(title:\s*)(.+)$", re.MULTILINE)


def unquote_yaml(s: str) -> str:
    s = s.strip()
    if len(s) >= 2:
        if s[0] == '"' and s[-1] == '"':
            return s[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        if s[0] == "'" and s[-1] == "'":
            return s[1:-1].replace("''", "'")
    return s


def quote_yaml(s: str) -> str:
    """Return a safe double-quoted YAML scalar."""
    escaped = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def first_sentence(text: str) -> str:
    """
    Return the first sentence of text.
    Sentence boundary: ., !, ? followed by whitespace/end-of-string,
    with special care to not split on decimal numbers (1.5) or abbreviations
    like "e.g.".
    """
    # Priority: ! and ? are almost always sentence-ending
    m = re.search(r"[!?]", text)
    if m:
        return text[: m.end()].strip()

    # For period: must be followed by whitespace+uppercase, or end of string,
    # and NOT preceded by a digit (to avoid "17.0", "v1.5" etc.)
    m = re.search(r"(?<!\d)\.(?=\s+[А-ЯЁA-Z\u2014\u2013\u00AB«]|\s*$)", text)
    if m:
        return text[: m.end()].strip()

    # No clear sentence boundary → use entire line
    return text.strip()


def process_post(md_path: Path) -> str:
    raw = md_path.read_text(encoding="utf-8")

    if "source: vk" not in raw:
        return "skip:not_vk"

    m = FRONT_MATTER_RE.match(raw)
    if not m:
        return "skip:no_fm"

    fm, after_fm = m.group(1), m.group(2)

    # --- parse current title ---
    tm = TITLE_LINE_RE.search(fm)
    if not tm:
        return "skip:no_title"

    current_title = unquote_yaml(tm.group(2))

    # --- find first meaningful body line ---
    body_lines = after_fm.lstrip("\n").splitlines()
    first_text_idx = None
    for i, line in enumerate(body_lines):
        s = line.strip()
        if s and not s.startswith("http") and not s.startswith("["):
            first_text_idx = i
            break

    if first_text_idx is None:
        return "skip:no_body_text"

    first_line = body_lines[first_text_idx].strip()

    # --- detect auto-generated titles: body starts with the title text ---
    norm_title = re.sub(r"\s+", " ", current_title).lower().strip()
    norm_first = re.sub(r"\s+", " ", first_line).lower().strip()

    # Require the first line to start with the current title (at least 15 chars or all of it)
    check_len = min(len(norm_title), 40)
    if check_len < 5:
        return "skip:title_too_short"
    if not norm_first.startswith(norm_title[:check_len]):
        return "skip:body_doesnt_start_with_title"

    # --- extract new title (first sentence of the first line) ---
    new_title = first_sentence(first_line)

    # If already identical, nothing to do
    if new_title == current_title:
        return "skip:already_correct"

    # --- update front matter ---
    new_fm = TITLE_LINE_RE.sub(
        lambda mo: mo.group(1) + quote_yaml(new_title),
        fm,
    )

    # --- update body: remove the sentence from the start ---
    remaining = first_line[len(new_title):].lstrip(" \t")

    if remaining:
        # Sentence was in the middle of the line; keep the rest
        body_lines[first_text_idx] = remaining
    else:
        # Sentence was the whole line; remove it
        body_lines.pop(first_text_idx)
        # Drop any blank lines that now lead the body
        while body_lines and not body_lines[0].strip():
            body_lines.pop(0)

    new_body = "\n".join(body_lines)
    # Ensure a single blank line between front matter and body
    if new_body and not new_body.startswith("\n"):
        new_body = "\n" + new_body
    if not new_body.endswith("\n"):
        new_body += "\n"

    new_raw = f"---\n{new_fm}\n---\n{new_body}"
    md_path.write_text(new_raw, encoding="utf-8")
    return f"fixed: {current_title!r} → {new_title!r}"


def main() -> None:
    md_files = sorted(SITE_POSTS.glob("*.md"))
    stats: dict[str, int] = {}
    fixed = 0
    for md_path in md_files:
        result = process_post(md_path)
        key = result.split(":")[0]
        stats[key] = stats.get(key, 0) + 1
        if key == "fixed":
            fixed += 1
            print(f"  {md_path.name}\n    {result[len('fixed: '):]}")

    print(f"\nStats: {stats}")
    print(f"Fixed: {fixed}")


if __name__ == "__main__":
    main()
