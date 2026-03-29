#!/bin/bash
# Resolve all symlinks in the given directory (recursively)
# and replace them with real files containing the same data.

set -euo pipefail

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No color

# --- Check args ---
if [[ $# -lt 1 ]]; then
    echo -e "${RED}❌ Usage:${NC} $0 <directory>"
    exit 1
fi

DIR="$1"

if [[ ! -d "$DIR" ]]; then
    echo -e "${RED}❌ Error:${NC} '$DIR' is not a valid directory."
    exit 1
fi

echo -e "${YELLOW}🔍 Scanning directory:${NC} $DIR"
echo

# --- Process all symlinks recursively ---
find "$DIR" -type l | while read -r symlink; do
    target=$(readlink "$symlink")

    # Resolve relative paths
    if [[ "$target" != /* ]]; then
        target="$(dirname "$symlink")/$target"
    fi

    if [[ ! -e "$target" ]]; then
        echo -e "${YELLOW}⚠️  Skipping broken symlink:${NC} $symlink"
        continue
    fi

    echo -e "${GREEN}🧩 Converting:${NC} $symlink -> $target"

    tmpfile="${symlink}.real"

    cp -L "$symlink" "$tmpfile"
    rm "$symlink"
    mv "$tmpfile" "$symlink"
done

echo
echo -e "${GREEN}✅ Done!${NC} All symlinks under '$DIR' are now real files."
