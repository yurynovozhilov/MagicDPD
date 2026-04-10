#!/usr/bin/env python3
"""Remove duplicated post titles from the beginning of markdown bodies."""

from pathlib import Path
import re


POSTS_DIR = Path(__file__).resolve().parents[1] / "site" / "content" / "posts"
TITLE_RE = re.compile(r'^title:\s*"?(.+?)"?\s*$', re.MULTILINE)


def extract_front_matter_and_body(text: str) -> tuple[str | None, str]:
    if not text.startswith("---\n"):
        return None, text

    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text

    return text[: end + 5], text[end + 5 :]


def extract_title(front_matter: str) -> str | None:
    match = TITLE_RE.search(front_matter)
    return match.group(1).strip() if match else None


def strip_leading_duplicate_title(title: str, body: str) -> str:
    lines = body.splitlines()
    first_non_empty = None
    for idx, line in enumerate(lines):
        if line.strip():
            first_non_empty = idx
            break

    if first_non_empty is None:
        return body

    if lines[first_non_empty].strip().casefold() != title.strip().casefold():
        return body

    del lines[first_non_empty]
    while first_non_empty < len(lines) and not lines[first_non_empty].strip():
        del lines[first_non_empty]

    result = "\n".join(lines)
    if body.endswith("\n"):
        result += "\n"
    return result


def main() -> None:
    changed = 0
    for path in sorted(POSTS_DIR.glob("*.md")):
        original = path.read_text(encoding="utf-8")
        front_matter, body = extract_front_matter_and_body(original)
        if not front_matter:
            continue

        title = extract_title(front_matter)
        if not title:
            continue

        updated_body = strip_leading_duplicate_title(title, body)
        if updated_body == body:
            continue

        path.write_text(front_matter + updated_body, encoding="utf-8")
        changed += 1

    print(f"Updated {changed} post(s).")


if __name__ == "__main__":
    main()
