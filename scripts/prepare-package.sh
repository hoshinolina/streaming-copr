#!/bin/sh
set -e

[ -e hook_payload ] && cat hook_payload

rev="HEAD"
pkgname="$1"
if [ -z "$pkgname" ]; then
    pkgname="$COPR_PACKAGE"
fi
if [ -z "$pkgname" ]; then
    echo "No package name specified" >&2
    exit 1
fi
spec="${pkgname}.spec"
out="$PWD"

echo "Package name: $pkgname"

cd "$(dirname "$0")"/..

git branch -d _filter &>/dev/null || true
git branch _filter "$rev"
FILTER_BRANCH_SQUELCH_WARNING=1 \
    git filter-branch --subdirectory-filter "$pkgname" -- _filter
git worktree add "$out"/tree _filter
cd "$out"/tree
cp -r * ..
rpmautospec process-distgit "${pkgname}.spec" ../"${pkgname}.spec"
cd ..
spectool -g "$spec"
