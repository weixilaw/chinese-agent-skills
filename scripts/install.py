#!/usr/bin/env python3
"""chinese-agent-skills 一键安装器（零依赖，仅用 Python 标准库）.

用法：
    python3 scripts/install.py                  # 安装全部 skill 到已检测到的 AI 工具
    python3 scripts/install.py --skills contract-review,meeting-minutes
    python3 scripts/install.py --tools claude-code,codex
    python3 scripts/install.py list             # 列出本仓库自带的 skill
    python3 scripts/install.py tools            # 列出检测到的 AI 工具及技能目录
    python3 scripts/install.py remove <name>    # 从所有位置卸载某个 skill
    python3 scripts/install.py validate <dir>   # 按开放标准校验一个 skill 目录

技能目录数据来源：各工具官方文档（2026-10 核实），详见 README。
"""
import argparse
import os
import re
import shutil
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")
HOME = os.path.expanduser("~")


def _p(*parts):
    return os.path.join(HOME, *parts)


# 工具名 -> (检测标记目录, 个人技能目录列表)
# 检测逻辑：标记目录存在即视为"已安装该工具"
TOOLS = {
    "claude-code": ([_p(".claude")], [_p(".claude", "skills")]),
    "codex": ([_p(".codex")], [_p(".codex", "skills"), _p(".agents", "skills")]),
    "cursor": ([_p(".cursor")], [_p(".cursor", "skills"), _p(".agents", "skills")]),
    "gemini-cli": ([_p(".muse")], [_p(".muse", "skills"), _p(".agents", "skills")]),
    "opencode": ([_p(".config", "opencode")], [_p(".config", "opencode", "skills"), _p(".agents", "skills")]),
    "copilot": ([_p(".copilot")], [_p(".copilot", "skills"), _p(".agents", "skills")]),
    "openclaw": ([_p(".openclaw")], [_p(".openclaw", "skills")]),
    # 通用目录：多数新工具（Claude Code / Codex / Cursor / Gemini CLI / OpenCode / Copilot）
    # 都会读取 ~/.agents/skills，无需安装对应工具也可使用
    "universal": ([], [_p(".agents", "skills")]),
}


def detect_tools():
    """返回检测到的工具名列表（保持 TOOLS 定义顺序）。"""
    found = []
    for name, (markers, _dirs) in TOOLS.items():
        if name == "universal":
            continue
        if any(os.path.isdir(m) for m in markers):
            found.append(name)
    return found


def parse_frontmatter(skill_dir):
    """解析 SKILL.md 的 YAML frontmatter，返回 (dict, error)。不用第三方 yaml 库。"""
    md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(md):
        return None, "缺少 SKILL.md"
    with open(md, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return None, "SKILL.md 开头缺少 YAML frontmatter（--- 包裹）"
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.strip().startswith("#"):
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, None


def validate_skill(skill_dir):
    """按 Agent Skills 开放标准做基础校验，返回 error 列表（空 = 通过）。"""
    errors = []
    name = os.path.basename(os.path.normpath(skill_dir))
    fm, err = parse_frontmatter(skill_dir)
    if err:
        return [err]
    if not fm.get("name"):
        errors.append("frontmatter 缺少 name")
    elif fm["name"] != name:
        errors.append(f"frontmatter name={fm['name']!r} 与目录名 {name!r} 不一致")
    elif not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", fm["name"]) or len(fm["name"]) > 64:
        errors.append("name 须为小写字母/数字/连字符，不超过 64 字符")
    desc = fm.get("description", "")
    if not desc:
        errors.append("frontmatter 缺少 description")
    elif len(desc) > 1024:
        errors.append(f"description {len(desc)} 字符，超过 1024 上限")
    return errors


def bundled_skills():
    """返回仓库自带的 skill 名列表。"""
    if not os.path.isdir(SKILLS_DIR):
        return []
    return sorted(
        d for d in os.listdir(SKILLS_DIR)
        if os.path.isdir(os.path.join(SKILLS_DIR, d)) and not d.startswith(".")
    )


def target_dirs(tool_names):
    """给定工具名，返回去重后的目标技能目录列表。"""
    dirs, seen = [], set()
    for t in tool_names:
        for d in TOOLS[t][1]:
            if d not in seen:
                seen.add(d)
                dirs.append(d)
    return dirs


def cmd_list(_args):
    skills = bundled_skills()
    print(f"本仓库自带 {len(skills)} 个 skill：")
    for s in skills:
        fm, _ = parse_frontmatter(os.path.join(SKILLS_DIR, s))
        desc = (fm or {}).get("description", "")
        print(f"  - {s}\n    {desc[:90]}")


def cmd_tools(_args):
    detected = set(detect_tools())
    print("AI 工具检测结果：")
    for name, (markers, dirs) in TOOLS.items():
        if name == "universal":
            print(f"  [通用] universal -> {', '.join(dirs)}（多数工具都会读取）")
            continue
        status = "已安装" if name in detected else "未检测到"
        print(f"  [{status}] {name} -> {', '.join(dirs)}")


def install_skill(name, dirs, force=False, dry_run=False):
    src = os.path.join(SKILLS_DIR, name)
    errs = validate_skill(src)
    if errs:
        print(f"  ! {name} 校验未通过，跳过：{'; '.join(errs)}")
        return 0
    done = 0
    for d in dirs:
        dest = os.path.join(d, name)
        if os.path.exists(dest) and not force:
            print(f"  - {dest} 已存在，跳过（加 --force 覆盖）")
            continue
        if dry_run:
            print(f"  + {dest}（预演）")
            done += 1
            continue
        os.makedirs(d, exist_ok=True)
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        print(f"  + {dest}")
        done += 1
    return done


def cmd_install(args):
    skills = bundled_skills()
    if args.skills:
        wanted = [s.strip() for s in args.skills.split(",") if s.strip()]
        unknown = [s for s in wanted if s not in skills]
        if unknown:
            print(f"未知的 skill：{', '.join(unknown)}（可用 list 查看）")
            return 1
        skills = wanted
    tools = detect_tools()
    if args.tools:
        wanted = [t.strip() for t in args.tools.split(",") if t.strip()]
        unknown = [t for t in wanted if t not in TOOLS]
        if unknown:
            print(f"未知的工具：{', '.join(unknown)}（可用 tools 查看）")
            return 1
        tools = wanted
    if not tools:
        print("未检测到任何 AI 工具，将安装到通用目录 ~/.agents/skills（多数工具都会读取）。")
        tools = ["universal"]
    dirs = target_dirs(tools)
    print(f"目标工具：{', '.join(tools)}")
    if not args.yes and not args.dry_run:
        ans = input(f"将安装 {len(skills)} 个 skill 到 {len(dirs)} 个目录，继续？[Y/n] ").strip().lower()
        if ans not in ("", "y", "yes"):
            print("已取消。")
            return 0
    total = 0
    for s in skills:
        print(f"[{s}]")
        total += install_skill(s, dirs, force=args.force, dry_run=args.dry_run)
    print(f"完成：{total} 处安装。" + ("（预演，未实际写入）" if args.dry_run else "重启 AI 工具后生效。"))
    return 0


def cmd_remove(args):
    name = args.name
    tool_filter = None
    if getattr(args, "tools", None):
        wanted = [t.strip() for t in args.tools.split(",") if t.strip()]
        unknown = [t for t in wanted if t not in TOOLS]
        if unknown:
            print(f"未知的工具：{', '.join(unknown)}（可用 tools 查看）")
            return 1
        tool_filter = wanted
    removed = 0
    for tool, (_markers, dirs) in TOOLS.items():
        if tool_filter and tool not in tool_filter:
            continue
        for d in dirs:
            dest = os.path.join(d, name)
            if os.path.isdir(dest):
                shutil.rmtree(dest)
                print(f"  - 已删除 {dest}")
                removed += 1
    print(f"完成：删除 {removed} 处。" if removed else f"未找到已安装的 {name}。")
    return 0


def cmd_validate(args):
    errs = validate_skill(os.path.abspath(args.dir))
    if errs:
        print("校验未通过：")
        for e in errs:
            print(f"  ! {e}")
        return 1
    print("校验通过：符合 Agent Skills 开放标准基础要求。")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="chinese-agent-skills 一键安装器")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("list", help="列出本仓库自带的 skill")
    sub.add_parser("tools", help="列出检测到的 AI 工具及技能目录")
    p_rm = sub.add_parser("remove", help="卸载某个 skill")
    p_rm.add_argument("name")
    p_rm.add_argument("--tools", help="只从指定工具的目录卸载，逗号分隔（默认扫描全部位置）")
    p_v = sub.add_parser("validate", help="校验一个 skill 目录")
    p_v.add_argument("dir")
    p_in = sub.add_parser("install", help="安装 skill（默认命令）")
    p_in.add_argument("--skills", help="只安装指定的 skill，逗号分隔（默认全部）")
    p_in.add_argument("--tools", help="只安装到指定的工具，逗号分隔（默认自动检测）")
    p_in.add_argument("--force", action="store_true", help="覆盖已存在的安装")
    p_in.add_argument("--yes", "-y", action="store_true", help="跳过确认")
    p_in.add_argument("--dry-run", action="store_true", help="只预演，不实际写入")
    # 允许省略 install 子命令：install.py --skills x / install.py -y
    # 注意：只有当子命令未被识别（cmd is None）时才回退为 install，
    # 避免把 remove/validate 等已有子命令的额外参数误判。
    args, _unknown = ap.parse_known_args(argv)
    if args.cmd is None:
        # argv 为 None 时必须回退到 sys.argv[1:]，否则真正的命令行参数会被丢弃
        raw = sys.argv[1:] if argv is None else argv
        args = ap.parse_args(["install"] + raw)
    return {"list": cmd_list, "tools": cmd_tools, "install": cmd_install,
            "remove": cmd_remove, "validate": cmd_validate}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
