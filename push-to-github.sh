#!/bin/bash
# GitHub Push Script for 4Seasons-Website
# Vervang YOUR_GITHUB_USERNAME met je GitHub username

GITHUB_USERNAME="YOUR_GITHUB_USERNAME"
REPO_NAME="4Seasonscleaning-Website"

echo "🚀 Pushing 4Seasons to GitHub..."
echo ""

# Set remote origin
git remote add origin https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main

echo ""
echo "✅ Push complete!"
echo ""
echo "Repository URL: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
echo "Share this link with your client for review"
