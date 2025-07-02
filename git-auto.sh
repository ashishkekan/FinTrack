#!/bin/bash

# Usage: ./git-auto.sh "your commit message"

# Exit if no commit message is provided
if [ -z "$1" ]; then
  echo "❌ Commit message is required."
  echo "Usage: ./git-auto.sh \"Your message\""
  exit 1
fi

# Detect current branch
branch=$(git rev-parse --abbrev-ref HEAD)

# Git operations
echo "🔍 Adding changes..."
git add .

echo "📝 Committing to branch '$branch'..."
git commit -m "$1"

echo "🚀 Pushing to $branch..."
git push origin "$branch"

echo "✅ Done on branch '$branch'!"
