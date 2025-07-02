#!/bin/bash

# Usage: ./git-auto.sh "your commit message"

# Exit if no commit message is provided
if [ -z "$1" ]; then
  echo "❌ Commit message is required."
  echo "Usage: ./git-auto.sh \"Your message\""
  exit 1
fi

# Git operations
echo "🔍 Adding changes..."
git add .

echo "📝 Committing..."
git commit -m "$1"

echo "🚀 Pushing to master..."
git push origin main

echo "✅ Done!"
