#!/usr/bin/env python3
"""
Translate Russian blog posts to technical English using Claude Haiku 4.5
via the `claude -p` CLI (no API key required — uses Claude Code subscription).

Usage:
    python translate_posts.py [--limit N] [--year YYYY ...]
"""

import json
import subprocess
import time
import argparse
from pathlib import Path

import frontmatter

POSTS_DIR = Path("site/content/posts")
OUTPUT_DIR = Path("site/content/posts")   # same dir as source
PROGRESS_FILE = Path("scripts/translate_progress.json")
MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = """\
You are a professional translator specializing in CAE/FEA/CFD simulation engineering.
Translate the following Russian text to technical English.

Rules:
- Output ONLY the translated text, no commentary or explanations
- Preserve all Markdown syntax exactly (headings, lists, bold, italic, links, images)
- Preserve all URLs verbatim
- Preserve code blocks (fenced and inline) verbatim
- Preserve product and company names exactly: ANSYS, LS-DYNA, COMSOL, Abaqus, OpenFOAM, \
SolidWorks, Altair, HyperMesh, Nastran, RADIOSS, STAR-CCM+, SimScale, LSTC, Oasys, \
MSC Software, Dassault Systèmes, Siemens, ESI Group, Hexagon, BETA CAE, ANSA, META, \
Femap, Patran, Marc, Adams, Fluent, CFX, Mechanical, SpaceClaim, Discovery, Converge, \
FLOW-3D, Moldex3D, Moldflow, Digimat, nCode, FEMFAT, OptiStruct, AcuSolve, Simcenter, \
NX, Creo, CATIA, Inventor, Fusion 360, MATLAB, Simulink, CalculiX, Salome-Meca, Code_Aster, \
Rocky DEM, EDEM, LIGGGHTS, DualSPHysics, PrePoMax, FEBio, TexGen, Paraview, EnSight, Tecplot
- Preserve emoji characters verbatim
- Use accurate technical terminology for simulation engineering"""


class RateLimitError(Exception):
    pass


def load_progress() -> set[str]:
    """Load set of already-translated filenames from progress file."""
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()


def save_progress(done: set[str]) -> None:
    """Atomically write progress set as sorted JSON list."""
    tmp = PROGRESS_FILE.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(sorted(done), f, indent=2)
    tmp.replace(PROGRESS_FILE)


def translate_text(text: str) -> str:
    """Translate text via `claude -p`, using Claude Code subscription auth."""
    if not text or not text.strip():
        return text

    prompt = f"{SYSTEM_PROMPT}\n\n{text}"

    result = subprocess.run(
        ["claude", "-p", prompt, "--model", MODEL],
        capture_output=True,
        text=True,
        timeout=120,
    )

    output = result.stdout + result.stderr
    if "You've hit your limit" in output or "rate limit" in output.lower():
        raise RateLimitError(output)

    if result.returncode != 0:
        raise RuntimeError(f"claude exited {result.returncode}: {result.stderr.strip()}")

    return result.stdout.strip()


def translate_post(md_path: Path) -> None:
    """Load a post, translate title and body, write to OUTPUT_DIR."""
    post = frontmatter.load(md_path)

    title = post.metadata.get("title", "")
    if title:
        post.metadata["title"] = translate_text(title)

    if post.content:
        post.content = translate_text(post.content)

    out_path = OUTPUT_DIR / (md_path.stem + ".en.md")
    with open(out_path, "w", encoding="utf-8") as f:
        frontmatter.dump(post, f)


def main():
    parser = argparse.ArgumentParser(description="Translate Russian posts to English")
    parser.add_argument("--limit", type=int, default=None, help="Stop after N translations")
    parser.add_argument("--year", action="append", help="Filter by year prefix (repeatable)")
    args = parser.parse_args()

    done = load_progress()
    md_files = sorted(p for p in POSTS_DIR.glob("*.md") if not p.name.endswith(".en.md"))

    if args.year:
        prefixes = tuple(f"{y}-" for y in args.year)
        md_files = [f for f in md_files if f.name.startswith(prefixes)]

    total = len(md_files)
    translated = 0

    for i, md_file in enumerate(md_files, 1):
        if md_file.name in done:
            continue

        if args.limit is not None and translated >= args.limit:
            break

        print(f"[{i}/{total}] {md_file.name}")

        try:
            translate_post(md_file)
            done.add(md_file.name)
            save_progress(done)
            translated += 1
        except RateLimitError:
            print("  Rate limited, waiting 60s and retrying...")
            time.sleep(60)
            try:
                translate_post(md_file)
                done.add(md_file.name)
                save_progress(done)
                translated += 1
            except Exception as e:
                print(f"  Error on retry: {e}")
        except Exception as e:
            print(f"  Error: {e}")

    print(f"Done. Translated {translated} posts. Total in progress: {len(done)}")


if __name__ == "__main__":
    main()
