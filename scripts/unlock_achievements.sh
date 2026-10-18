#!/usr/bin/env bash
# ==============================================================================
# GitHub Achievement Automation & Unlock Toolkit
# Target Account: lak-is-law (or any authenticated GitHub account)
# ==============================================================================
# This script guides and automates unlocking major GitHub achievements:
#   1. Pair Extraordinaire (Default, Bronze, Silver, Gold)
#   2. Pull Shark (Bronze, Silver, Gold)
#   3. Quickdraw
#   4. YOLO
# ==============================================================================

set -euo pipefail

# ANSI Colors
CYAN="\033[1;36m"
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
MAGENTA="\033[1;35m"
RED="\033[1;31m"
RESET="\033[0m"

echo -e "${CYAN}=====================================================${RESET}"
echo -e "${MAGENTA}   🏆 GitHub Achievements Unlock Toolkit 🏆${RESET}"
echo -e "${CYAN}=====================================================${RESET}"

# Check for gh CLI
if ! command -v gh &> /dev/null; then
  echo -e "${RED}[!] GitHub CLI ('gh') is not installed.${RESET}"
  echo "Please install it: brew install gh"
  exit 1
fi

# Check authentication
echo -e "\n${YELLOW}[*] Verifying GitHub CLI authentication...${RESET}"
if ! gh auth status &> /dev/null; then
  echo -e "${RED}[!] Not currently logged in to GitHub CLI.${RESET}"
  echo -e "${YELLOW}Please authenticate by running:${RESET} gh auth login"
  echo "After authenticating, re-run this script."
  exit 1
fi

CURRENT_USER=$(gh api user --jq '.login' 2>/dev/null || echo "lak-is-law")
echo -e "${GREEN}[✔] Authenticated as:${RESET} ${CURRENT_USER}"

echo -e "\n${CYAN}Select an action to unlock:${RESET}"
echo "1) [Pair Extraordinaire] Unlock with 1 Co-authored Merged PR"
echo "2) [Pull Shark + Pair Extraordinaire] Fast-track batch PR merges (Silver / Gold)"
echo "3) [Quickdraw] Open and close an issue/PR within 5 seconds"
echo "4) [YOLO] Merge a PR without review"
echo "5) [Full Package] Run Quickdraw + YOLO + Pair Extraordinaire on a scratch repo"
echo "6) View manual guide for Galaxy Brain, Public Sponsor & Starstruck"
echo "q) Quit"
echo ""

read -rp "Enter choice [1-6, q]: " CHOICE

TEMP_DIR=$(mktemp -d /tmp/gh-achieve-XXXXXX)
trap 'rm -rf "$TEMP_DIR"' EXIT

case "$CHOICE" in
  1)
    echo -e "\n${MAGENTA}--- Unlocking Pair Extraordinaire ---${RESET}"
    read -rp "Enter repository name (e.g., lak-is-law/achievements-sandbox or lak-is-law/lak-is-law): " TARGET_REPO
    TARGET_REPO=${TARGET_REPO:-"lak-is-law/lak-is-law"}

    cd "$TEMP_DIR"
    gh repo clone "$TARGET_REPO" repo
    cd repo

    BRANCH_NAME="pair-achievement-$(date +%s)"
    git checkout -b "$BRANCH_NAME"

    echo "Pair Extraordinaire unlock stamp: $(date)" >> .github-achievement.log
    git add .github-achievement.log

    # The magic Co-authored-by trailer that GitHub uses to award Pair Extraordinaire
    git commit -m "feat: collaborate on repository

Co-authored-by: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>"

    git push origin "$BRANCH_NAME"
    PR_URL=$(gh pr create --repo "$TARGET_REPO" --head "$BRANCH_NAME" --base main --title "feat: unlock pair extraordinaire" --body "Co-authored commit for achievement")
    echo -e "${GREEN}[✔] PR created:${RESET} $PR_URL"

    # Merge PR
    gh pr merge "$PR_URL" --repo "$TARGET_REPO" --merge --delete-branch
    echo -e "${GREEN}🎉 Successfully merged! Check https://github.com/${CURRENT_USER}?tab=achievements in a few moments!${RESET}"
    ;;

  2)
    echo -e "\n${MAGENTA}--- Fast-Track Pull Shark & Pair Extraordinaire ---${RESET}"
    echo "This will create a dedicated sandbox repository and merge small PRs with co-author trailers."
    read -rp "How many PRs to merge? (e.g. 16 for Silver, 128 for Gold): " COUNT
    COUNT=${COUNT:-16}

    SANDBOX_REPO="achievement-sandbox"
    echo -e "${YELLOW}[*] Setting up sandbox repository '${CURRENT_USER}/${SANDBOX_REPO}'...${RESET}"

    if ! gh repo view "${CURRENT_USER}/${SANDBOX_REPO}" &> /dev/null; then
      gh repo create "${CURRENT_USER}/${SANDBOX_REPO}" --public --init
    fi

    cd "$TEMP_DIR"
    gh repo clone "${CURRENT_USER}/${SANDBOX_REPO}" repo
    cd repo

    for ((i=1; i<=COUNT; i++)); do
      BRANCH="achieve-$i-$(date +%s)"
      git checkout -b "$BRANCH" main
      echo "PR iteration $i at $(date)" >> progress.txt
      git add progress.txt
      git commit -m "chore: progress iteration $i

Co-authored-by: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>"
      git push origin "$BRANCH" -q
      PR=$(gh pr create --title "Iteration $i" --body "Automated achievement step" --base main --head "$BRANCH")
      gh pr merge "$PR" --merge --delete-branch
      echo -e "${GREEN}[$i/$COUNT] Merged PR:${RESET} $PR"
      sleep 2
    done

    echo -e "${GREEN}🎉 Completed $COUNT merges! Pull Shark & Pair Extraordinaire tier upgrades unlocked!${RESET}"
    ;;

  3)
    echo -e "\n${MAGENTA}--- Unlocking Quickdraw ---${RESET}"
    read -rp "Enter target repository (e.g. lak-is-law/lak-is-law): " TARGET_REPO
    TARGET_REPO=${TARGET_REPO:-"lak-is-law/lak-is-law"}

    ISSUE_URL=$(gh issue create --repo "$TARGET_REPO" --title "Temporary Quickdraw Issue" --body "Will be closed in 5 seconds.")
    echo -e "${YELLOW}[*] Created issue:${RESET} $ISSUE_URL"
    sleep 3
    gh issue close "$ISSUE_URL" --repo "$TARGET_REPO" --reason "completed"
    echo -e "${GREEN}🎉 Closed immediately! Quickdraw achievement unlocked!${RESET}"
    ;;

  4)
    echo -e "\n${MAGENTA}--- Unlocking YOLO ---${RESET}"
    read -rp "Enter target repository (e.g. lak-is-law/lak-is-law): " TARGET_REPO
    TARGET_REPO=${TARGET_REPO:-"lak-is-law/lak-is-law"}

    cd "$TEMP_DIR"
    gh repo clone "$TARGET_REPO" repo
    cd repo
    BRANCH="yolo-$(date +%s)"
    git checkout -b "$BRANCH"
    echo "yolo stamp $(date)" >> .yolo
    git add .yolo
    git commit -m "yolo: merge without review"
    git push origin "$BRANCH"
    PR_URL=$(gh pr create --repo "$TARGET_REPO" --title "YOLO run" --body "Direct merge" --base main --head "$BRANCH")
    gh pr merge "$PR_URL" --repo "$TARGET_REPO" --merge --delete-branch
    echo -e "${GREEN}🎉 YOLO merged without review! Achievement unlocked!${RESET}"
    ;;

  5)
    echo -e "\n${MAGENTA}--- Full Package Sandbox Unlock ---${RESET}"
    SANDBOX_REPO="achievements-sandbox"
    echo -e "${YELLOW}[*] Initializing sandbox repo '${CURRENT_USER}/${SANDBOX_REPO}'...${RESET}"
    gh repo create "${CURRENT_USER}/${SANDBOX_REPO}" --public --init || true

    cd "$TEMP_DIR"
    gh repo clone "${CURRENT_USER}/${SANDBOX_REPO}" repo
    cd repo

    # 1. Quickdraw
    echo -e "${YELLOW}[1/3] Triggering Quickdraw...${RESET}"
    ISSUE=$(gh issue create --repo "${CURRENT_USER}/${SANDBOX_REPO}" --title "Quickdraw test" --body "Closing immediately")
    sleep 2
    gh issue close "$ISSUE" --repo "${CURRENT_USER}/${SANDBOX_REPO}" --reason "completed"
    echo -e "${GREEN}[✔] Quickdraw complete.${RESET}"

    # 2. Pair Extraordinaire + YOLO
    echo -e "${YELLOW}[2/3] Triggering Pair Extraordinaire & YOLO...${RESET}"
    git checkout -b "coauthor-branch"
    echo "co-authored entry" >> README.md
    git add README.md
    git commit -m "feat: collaborate on docs

Co-authored-by: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>"
    git push origin coauthor-branch
    PR=$(gh pr create --repo "${CURRENT_USER}/${SANDBOX_REPO}" --title "Pair & YOLO unlock" --body "Co-authored PR" --base main --head "coauthor-branch")
    gh pr merge "$PR" --repo "${CURRENT_USER}/${SANDBOX_REPO}" --merge --delete-branch
    echo -e "${GREEN}[✔] Pair Extraordinaire & YOLO merged.${RESET}"

    echo -e "\n${GREEN}🎉 Sandbox execution complete! Check your profile achievements: https://github.com/${CURRENT_USER}?tab=achievements${RESET}"
    ;;

  6)
    echo -e "\n${CYAN}=====================================================${RESET}"
    echo -e "${MAGENTA}   Guide to Remaining Major Achievements${RESET}"
    echo -e "${CYAN}=====================================================${RESET}"
    echo -e "1. ${YELLOW}Galaxy Brain${RESET}:"
    echo "   - Enable 'Discussions' in any public repo (Settings -> Features -> Discussions)."
    echo "   - Create a question in the Q&A category."
    echo "   - Post a helpful answer from your account."
    echo "   - Mark that answer as 'Accepted Answer'."
    echo "   - 2 answers = Default, 8 = Silver, 16 = Gold."
    echo ""
    echo -e "2. ${YELLOW}Public Sponsor${RESET}:"
    echo "   - Go to https://github.com/sponsors/community"
    echo "   - Sponsor any favorite open source project or developer for \$1 (one-time or monthly)."
    echo "   - The badge unlocks immediately on your profile."
    echo ""
    echo -e "3. ${YELLOW}Starstruck${RESET}:"
    echo "   - Awarded when one of your repositories reaches 16 stars (Bronze), 128 (Silver), 512 (Gold)."
    echo "   - Showcase Skyward or Craftme on Reddit r/webdev, Product Hunt, and developer discords!"
    echo -e "${CYAN}=====================================================${RESET}"
    ;;

  *)
    echo "Exiting."
    exit 0
    ;;
esac
