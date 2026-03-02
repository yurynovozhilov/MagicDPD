#!/bin/bash
REPO_DIR="$(dirname "$0")"

echo "Fetching link previews..."
cd "$REPO_DIR"
python fetch_link_previews.py

echo "Starting Hugo server..."
cd "$REPO_DIR/site"
hugo server --disableFastRender --bind 0.0.0.0 --port 1313 -b http://localhost:1313/ &
echo $! > /tmp/magicdpd_hugo.pid
echo "Site started at http://localhost:1313"
