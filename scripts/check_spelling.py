#!/usr/bin/env python3
"""
Spell checking script for Russian Hugo blog posts.
Usage:
    python check_spelling.py --report [--limit N]     # Generate spelling report
    python check_spelling.py --fix [--dry-run]        # Auto-fix high-confidence errors
"""

import os
import re
import sys
import csv
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Set
import yaml

try:
    import enchant
    ENCHANT_AVAILABLE = True
except ImportError:
    ENCHANT_AVAILABLE = False
    print("Warning: enchant not available, spell checking may not work")


class SpellingChecker:
    def __init__(self, whitelist_path: str = None):
        """Initialize spell checker."""
        print("Initializing spell checker...")

        self.whitelist = set()
        if whitelist_path and os.path.exists(whitelist_path):
            self.whitelist = self.load_whitelist(whitelist_path)

        # Initialize enchant for Russian
        if ENCHANT_AVAILABLE:
            try:
                self.checker = enchant.DictWithPWL('ru_RU', whitelist_path) if whitelist_path else enchant.Dict('ru_RU')
            except:
                try:
                    self.checker = enchant.Dict('ru')
                except:
                    print("Error: Russian dictionary not found. Install: brew install aspell-ru")
                    self.checker = None
        else:
            self.checker = None

        self.posts_dir = Path('/Users/GlukRazor/MagicDPD/site/content/posts')
        self.errors = []

    def load_whitelist(self, whitelist_path: str) -> Set[str]:
        """Load technical terms whitelist."""
        whitelist = set()
        if os.path.exists(whitelist_path):
            with open(whitelist_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        whitelist.add(line.lower())
        return whitelist

    def clean_text(self, text: str) -> str:
        """Remove URLs, markdown links, code blocks, and other non-content."""
        cleaned = text

        # Remove URLs
        cleaned = re.sub(r'https?://[^\s\)]+', ' ', cleaned)
        cleaned = re.sub(r'ftp://[^\s\)]+', ' ', cleaned)

        # Remove markdown links [text](url) -> keep text
        cleaned = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', cleaned)

        # Remove hashtags
        cleaned = re.sub(r'#[\w_-]+', '', cleaned)

        # Remove inline code `code`
        cleaned = re.sub(r'`[^`]+`', ' ', cleaned)

        # Remove code blocks
        cleaned = re.sub(r'```[^`]*```', ' ', cleaned, flags=re.DOTALL)

        # Remove HTML tags
        cleaned = re.sub(r'<[^>]+>', ' ', cleaned)

        return cleaned

    def parse_post(self, file_path: Path) -> Tuple[str, str]:
        """Parse Hugo post and extract title and body."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None, None

        # Split frontmatter and body
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    title = frontmatter.get('title', '') if frontmatter else ''
                    body = parts[2].strip()
                    return title or '', body
                except yaml.YAMLError as e:
                    print(f"YAML parse error in {file_path}: {e}")
                    return None, None

        return '', content

    def is_whitelisted(self, word: str) -> bool:
        """Check if word is in technical terms whitelist."""
        word_lower = word.lower()

        # Check exact match
        if word_lower in self.whitelist:
            return True

        # Check if it's part of a known technical term (case-insensitive prefix)
        for term in self.whitelist:
            if word_lower in term.lower() or term.lower() in word_lower:
                return True

        return False

    def get_suggestions(self, word: str) -> List[str]:
        """Get spelling suggestions for a word."""
        if not self.checker:
            return []

        try:
            suggestions = self.checker.suggest(word)
            return suggestions[:5]  # Limit to 5 suggestions
        except:
            return []

    def check_text(self, text: str, source_file: str) -> List[Dict]:
        """Check spelling in text and return errors."""
        if not text or len(text.strip()) < 2:
            return []

        if not self.checker:
            return []

        # Clean text
        cleaned_text = self.clean_text(text)

        errors = []

        # Split into words and check each one
        words = re.findall(r'\b[\w\-]+\b', cleaned_text)

        for word in words:
            # Skip if too short or already whitelisted
            if len(word) < 3 or self.is_whitelisted(word):
                continue

            # Skip if it's a number or all caps (likely acronym)
            if word.isdigit() or (word.isupper() and len(word) <= 5):
                continue

            # Skip version strings (v1, v10, v2.04, etc.)
            if re.match(r'^v\d+(\.\d+)*$', word, re.IGNORECASE):
                continue

            # Skip numbered ordinals (1-ое, 2-ое, 3-й, etc.)
            if re.match(r'^\d+[\-\s]*(ое|ый|ий|й|я|го|му|ю)$', word, re.IGNORECASE):
                continue

            # Skip words with hyphens that look like formatting
            if '-' in word:
                parts = word.split('-')
                # Skip if parts look like version or numbering
                if any(p.isdigit() or len(p) == 1 for p in parts):
                    continue

            # Check if misspelled
            try:
                if not self.checker.check(word):
                    suggestions = self.get_suggestions(word)
                    if suggestions:
                        errors.append({
                            'file': str(source_file),
                            'word': word,
                            'context': cleaned_text[:100],
                            'suggestions': suggestions,
                            'confidence': len(suggestions) == 1,
                            'rule_id': 'SPELLING',
                        })
            except:
                pass

        return errors

    def check_all_posts(self, limit: int = None) -> List[Dict]:
        """Check all posts in the posts directory."""
        all_errors = []

        # Get all markdown files
        md_files = sorted(self.posts_dir.glob('*.md'))
        if limit:
            md_files = md_files[:limit]

        total = len(md_files)
        print(f"Checking {total} posts...")

        for i, md_file in enumerate(md_files, 1):
            if i % 100 == 0:
                print(f"  Progress: {i}/{total}")

            title, body = self.parse_post(md_file)
            if title is None:
                continue

            # Check title
            if title:
                errors = self.check_text(title, f"{md_file.name}:title")
                all_errors.extend(errors)

            # Check body
            if body:
                errors = self.check_text(body, f"{md_file.name}:body")
                all_errors.extend(errors)

        print(f"Found {len(all_errors)} potential spelling errors")
        return all_errors

    def generate_report(self, errors: List[Dict], output_file: str = 'spelling_report.csv'):
        """Generate CSV report of spelling errors."""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'file', 'word', 'context', 'suggestions', 'confidence', 'rule_id'
            ])
            writer.writeheader()

            for error in errors:
                writer.writerow({
                    'file': error['file'],
                    'word': error['word'],
                    'context': error['context'][:100],
                    'suggestions': ' | '.join(error['suggestions']),
                    'confidence': 'HIGH' if error['confidence'] else 'LOW',
                    'rule_id': error['rule_id'],
                })

        print(f"Report saved to {output_file}")
        return output_file

    def fix_posts(self, errors: List[Dict], dry_run: bool = False) -> int:
        """Apply high-confidence auto-fixes to posts."""
        # Filter to high-confidence errors only
        high_conf_errors = [e for e in errors if e['confidence']]

        if not high_conf_errors:
            print("No high-confidence errors to fix")
            return 0

        print(f"Found {len(high_conf_errors)} high-confidence errors to fix")

        # Group by file
        fixes_by_file = {}
        for error in high_conf_errors:
            file_name = error['file'].split(':')[0]
            if file_name not in fixes_by_file:
                fixes_by_file[file_name] = []
            fixes_by_file[file_name].append(error)

        total_fixes = 0

        for file_name, file_errors in fixes_by_file.items():
            file_path = self.posts_dir / file_name

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading {file_name}: {e}")
                continue

            original_content = content

            # Apply fixes (sort by position to avoid offset issues)
            for error in sorted(file_errors, key=lambda x: x['word']):
                old_word = error['word']
                new_word = error['suggestions'][0]

                # Simple replacement with word boundaries
                pattern = r'\b' + re.escape(old_word) + r'\b'
                content = re.sub(pattern, new_word, content, count=1)
                total_fixes += 1

                if dry_run:
                    print(f"  Would fix in {file_name}: {old_word} → {new_word}")
                else:
                    print(f"  Fixed in {file_name}: {old_word} → {new_word}")

            # Write back if not dry-run
            if not dry_run and content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

        if not dry_run and total_fixes > 0:
            # Create git commit
            print(f"\nCreating git commit for {total_fixes} spelling fixes...")
            try:
                subprocess.run(['git', 'add', str(self.posts_dir)], check=True, cwd='/Users/GlukRazor/MagicDPD')
                subprocess.run([
                    'git', 'commit', '-m',
                    f'Fix {total_fixes} spelling errors in posts\n\nAuto-corrected high-confidence typos using Enchant spell checker.'
                ], check=True, cwd='/Users/GlukRazor/MagicDPD')
                print("Commit created successfully")
            except subprocess.CalledProcessError as e:
                print(f"Error creating commit: {e}")

        return total_fixes


def main():
    parser = argparse.ArgumentParser(description='Check and fix spelling in Russian Hugo posts')
    parser.add_argument('--report', action='store_true', help='Generate spelling report (CSV)')
    parser.add_argument('--fix', action='store_true', help='Apply high-confidence auto-fixes')
    parser.add_argument('--limit', type=int, default=None, help='Limit to N posts (for testing)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be fixed without applying changes')

    args = parser.parse_args()

    if not args.report and not args.fix:
        parser.print_help()
        sys.exit(1)

    whitelist_path = '/Users/GlukRazor/MagicDPD/scripts/spelling_whitelist.txt'
    checker = SpellingChecker(whitelist_path)

    if not checker.checker:
        print("Error: No spell checker available")
        sys.exit(1)

    # Check all posts
    errors = checker.check_all_posts(limit=args.limit)

    if args.report:
        checker.generate_report(errors, 'spelling_report.csv')

    if args.fix:
        total_fixed = checker.fix_posts(errors, dry_run=args.dry_run)
        print(f"Total fixes applied: {total_fixed}")


if __name__ == '__main__':
    main()
