#!/bin/bash

# Usage:
# ./git-auto.sh "Commit message" file1 file2 file3 ...

# Check commit message
if [ -z "$1" ]; then
  echo "❌ Commit message is required."
  echo "Usage: ./git-auto.sh \"Your message\" file1 file2 ..."
  exit 1
fi

commit_msg="$1"
shift  # Shift parameters to get file list (from $2 onward)

# Check if any files are provided
if [ $# -eq 0 ]; then
  echo "❌ No files provided to add."
  echo "Usage: ./git-auto.sh \"Your message\" file1 file2 ..."
  exit 1
fi

# Detect current branch
branch=$(git rev-parse --abbrev-ref HEAD)

# Git operations
echo "🔍 Adding files: $@"
git add "$@"

echo "📝 Committing to branch '$branch'..."
git commit -m "$commit_msg"

echo "🚀 Pushing to $branch..."
git push origin "$branch"

echo "✅ Done on branch '$branch'!"
