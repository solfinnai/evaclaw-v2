#!/bin/bash
# Push updated v4.3 files to GitHub
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_DIR"

echo "=== Pushing updated v4.3 to GitHub ==="

# Clean up any existing .git directory
if [ -d ".git" ]; then
    rm -rf .git
fi

# Save local files to temp before git overwrites them
echo "Saving local files..."
TMPDIR=$(mktemp -d)
cp -r . "$TMPDIR/"

# Initialize fresh git repo
git init
git branch -m main
git config user.email "henryfinnai@gmail.com"
git config user.name "solfinnai"

# Add remote and fetch
git remote add origin https://github.com/solfinnai/evaclaw-v2.git
echo "Fetching existing repo..."
git fetch origin master

# Checkout existing repo (overwrites local files)
git checkout -f -b main origin/master

# Restore ALL local files back on top
echo "Restoring local files..."
rsync -a --exclude='.git' --exclude='push-to-github.sh' --exclude='evaclaw-v4.3.bundle' --exclude='.DS_Store' --exclude='__pycache__' --exclude='*.db' --exclude='*.db-journal' "$TMPDIR/" ./

# Clean up temp
rm -rf "$TMPDIR"

# Stage everything
git add -A

echo ""
echo "Files staged:"
git status --short
echo ""

# Commit
git commit -m "Update download package to v4.3 with OAuth auth flow

- Replaced old staticFiles templates with actual v4.3 file contents
- Updated generateAndDownload() for v4.3 folder structure
- Install instructions now use claude setup-token OAuth flow
- Removed old SYSTEM.md, BOOT-SEQUENCE.md, DELEGATION.md templates
- Added all v4.3 files: AGENTS-REFERENCE.md, shipping/, docs/, etc."

# Push
echo "Pushing to GitHub..."
git push origin main:master

echo ""
echo "=== Done! Updated files pushed to GitHub ==="
echo "Check: https://github.com/solfinnai/evaclaw-v2"

# Cleanup
rm -f push-to-github.sh evaclaw-v4.3.bundle
