#!/bin/sh
set -e

[ -e hook_payload ] && cat hook_payload

rev="HEAD"
pkgname="$COPR_PACKAGE"
out="$PWD"
cd "$(dirname "$0")"/..

git branch -d _filter &>/dev/null || true
git branch _filter "$rev"
FILTER_BRANCH_SQUELCH_WARNING=1 \
    git filter-branch --subdirectory-filter "$pkgname" -- _filter
git worktree add "$out" _filter
cd "$out"
rpmautospec process-distgit "${pkgname}.spec" "${pkgname}.spec"
