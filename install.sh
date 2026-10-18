#!/usr/bin/env bash
# chinese-agent-skills 一键安装 bootstrap（零依赖，只需要 python3）
#
# 一键安装：
#   curl -fsSL https://raw.githubusercontent.com/weixilaw/chinese-agent-skills/main/install.sh | bash
#
# 带参数（会透传给 scripts/install.py）：
#   curl -fsSL https://raw.githubusercontent.com/weixilaw/chinese-agent-skills/main/install.sh | bash -s -- --skills contract-review -y
#
# 安装前请先阅读本脚本与 scripts/install.py，确认你信任其内容。
set -euo pipefail

REPO_URL="https://github.com/weixilaw/chinese-agent-skills.git"
TARBALL_URL="https://codeload.github.com/weixilaw/chinese-agent-skills/tar.gz/refs/heads/main"

command -v python3 >/dev/null 2>&1 || {
    echo "错误：需要 python3，请先安装 Python 3（https://www.python.org/downloads/）。" >&2
    exit 1
}

WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

echo "==> 下载 chinese-agent-skills ..."
if command -v git >/dev/null 2>&1 && git clone --depth 1 "$REPO_URL" "$WORKDIR/repo" >/dev/null 2>&1; then
    echo "    via git clone"
elif command -v curl >/dev/null 2>&1 && curl -fsSL "$TARBALL_URL" -o "$WORKDIR/repo.tar.gz"; then
    echo "    via tarball"
    mkdir -p "$WORKDIR/repo"
    tar -xzf "$WORKDIR/repo.tar.gz" -C "$WORKDIR/repo" --strip-components=1
else
    echo "错误：下载失败，需要 git 或 curl 其中之一。" >&2
    exit 1
fi

python3 "$WORKDIR/repo/scripts/install.py" "$@"
