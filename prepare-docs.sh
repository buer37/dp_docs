#!/usr/bin/env bash
# 构建前把文档同步到 docs/（MkDocs 要求 docs_dir 为子目录）
# 用法：bash prepare-docs.sh  或  ./prepare-docs.sh（Git Bash / WSL）
set -e
mkdir -p docs
cp *.md docs/ 2>/dev/null || true
for d in */; do
  [ "$d" = "docs/" ] && continue
  cp -r "$d" docs/
done
echo "docs/ 已就绪"
