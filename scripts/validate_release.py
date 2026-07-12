#!/usr/bin/env python3
"""验证多平台公开发布包，不访问网络也不修改文件。"""

from __future__ import annotations

import json
import re
import struct
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

REQUIRED = [
    ".codex-plugin/plugin.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    "skills/generate-ai-career-roadmap/SKILL.md",
    "skills/generate-ai-career-roadmap/references/intake-profile.md",
    "skills/generate-ai-career-roadmap/references/research-policy.md",
    "skills/generate-ai-career-roadmap/references/role-taxonomy.md",
    "skills/generate-ai-career-roadmap/references/learning-plan-framework.md",
    "skills/generate-ai-career-roadmap/references/report-contract.md",
    "assets/logo.svg",
    "assets/logo.png",
    "assets/icon.png",
    "README.md",
    "LICENSE",
    "PRIVACY.md",
    "TERMS.md",
    "docs/index.html",
    "docs/privacy.html",
    "docs/terms.html",
    "docs/support.html",
    "docs/assets/logo.svg",
    "docs/assets/icon.png",
    ".github/workflows/pages.yml",
    ".github/workflows/validate.yml",
    "submissions/openai/test-cases.md",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def read_json(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(errors, f"JSON无效：{path.relative_to(ROOT)}：{exc}")
        return {}


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("不是PNG")
    return struct.unpack(">II", data[16:24])


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            fail(errors, f"缺少文件：{relative}")

    codex = read_json(ROOT / ".codex-plugin/plugin.json", errors)
    claude = read_json(ROOT / ".claude-plugin/plugin.json", errors)
    marketplace = read_json(ROOT / ".claude-plugin/marketplace.json", errors)

    if codex.get("name") != "ai-career-roadmap-skill":
        fail(errors, "Codex插件名称不正确。")
    if codex.get("version") != VERSION or claude.get("version") != VERSION:
        fail(errors, "插件版本与VERSION不一致。")
    if codex.get("license") != "MIT-0" or claude.get("license") != "MIT-0":
        fail(errors, "公开版本必须统一使用MIT-0。")
    if codex.get("author", {}).get("name") != "yxn否定我":
        fail(errors, "Codex发布者名称不正确。")
    if not marketplace.get("plugins"):
        fail(errors, "Claude市场清单没有插件条目。")

    interface = codex.get("interface", {})
    for key in (
        "displayName", "shortDescription", "longDescription", "developerName",
        "category", "websiteURL", "privacyPolicyURL", "termsOfServiceURL",
        "defaultPrompt", "composerIcon", "logo",
    ):
        if not interface.get(key):
            fail(errors, f"Codex界面字段缺失：{key}")
    if not isinstance(interface.get("defaultPrompt"), list) or len(interface.get("defaultPrompt", [])) != 3:
        fail(errors, "Codex Starter Prompts 必须正好3条。")

    skill_text = (ROOT / "skills/generate-ai-career-roadmap/SKILL.md").read_text(encoding="utf-8")
    if not re.search(r"^name:\s*generate-ai-career-roadmap\s*$", skill_text, re.MULTILINE):
        fail(errors, "Skill名称或frontmatter不正确。")
    if "description:" not in skill_text[:1000]:
        fail(errors, "Skill缺少description。")

    tests = (ROOT / "submissions/openai/test-cases.md").read_text(encoding="utf-8")
    positive = len(re.findall(r"^###\s+[1-5]\.\s+", tests, re.MULTILINE))
    negative_section = tests.split("## 负向测试：共3个", 1)
    negative = 0 if len(negative_section) != 2 else len(
        re.findall(r"^###\s+[1-3]\.\s+", negative_section[1], re.MULTILINE)
    )
    if positive != 8 or negative != 3:
        # 正向标题和负向标题都使用数字；全文应有8个，负向段应有3个。
        fail(errors, f"审核测试数量不正确：全部编号标题{positive}，负向{negative}。")

    scan_suffixes = {".md", ".json", ".yaml", ".yml", ".html", ".css", ".py", ".txt"}
    forbidden = [
        (re.compile(r"杨向南|Yang Xiangnan", re.IGNORECASE), "旧使用者姓名"),
        (re.compile(r"[A-Z]:\\(?:Users|Code)\\", re.IGNORECASE), "本地绝对路径"),
        (re.compile(r"\b(?:ghp|github_pat|clh)_[A-Za-z0-9_\-]{12,}"), "访问令牌"),
        (re.compile(r"\[TODO[^\]]*\]", re.IGNORECASE), "TODO占位符"),
    ]
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in scan_suffixes or path == Path(__file__):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern, label in forbidden:
            if pattern.search(text):
                fail(errors, f"发现{label}：{path.relative_to(ROOT)}")

    for relative, expected in [("assets/logo.png", (512, 512)), ("assets/icon.png", (256, 256))]:
        try:
            actual = png_size(ROOT / relative)
            if actual != expected:
                fail(errors, f"图标尺寸错误：{relative}={actual}，应为{expected}")
        except Exception as exc:
            fail(errors, f"图标无效：{relative}：{exc}")

    for page in (ROOT / "docs").glob("*.html"):
        html = page.read_text(encoding="utf-8")
        for target in re.findall(r'(?:href|src)="([^"]+)"', html):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            local = (page.parent / target.split("#", 1)[0]).resolve()
            if not local.is_file():
                fail(errors, f"官网本地链接失效：{page.name} -> {target}")

    validator = ROOT / "skills/generate-ai-career-roadmap/scripts/validate_career_report.py"
    test = subprocess.run(
        [sys.executable, str(validator), "--self-test"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if test.returncode != 0:
        fail(errors, "职业报告校验器自测失败。")

    if errors:
        print("发布前检查：失败")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("发布前检查：通过")
    print(f"版本：{VERSION}；必备文件：{len(REQUIRED)}；审核测试：5个正向、3个负向。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
