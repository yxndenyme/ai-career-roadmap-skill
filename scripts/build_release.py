#!/usr/bin/env python3
"""生成OpenAI、Claude、通用Skill和扣子发布ZIP。"""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
OUT = ROOT / "release"


def files_under(relative: str):
    base = ROOT / relative
    return [path for path in base.rglob("*") if path.is_file()]


def write_zip(output: Path, entries: list[tuple[Path, str]]) -> None:
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source, target in sorted(entries, key=lambda item: item[1]):
            archive.write(source, target)
    print(f"Generated: {output.name}")


def main() -> int:
    check = subprocess.run([sys.executable, str(ROOT / "scripts/validate_release.py")])
    if check.returncode != 0:
        return check.returncode

    OUT.mkdir(exist_ok=True)
    common_docs = [ROOT / name for name in ("README.md", "LICENSE", "PRIVACY.md", "TERMS.md")]

    openai_entries = [(path, path.relative_to(ROOT).as_posix()) for path in (
        files_under(".codex-plugin") + files_under("assets") + files_under("skills") + common_docs
    )]
    write_zip(OUT / f"openai-ai-career-roadmap-skill-{VERSION}.zip", openai_entries)

    claude_entries = [(path, path.relative_to(ROOT).as_posix()) for path in (
        files_under(".claude-plugin") + files_under("assets") + files_under("skills") + common_docs
    )]
    write_zip(OUT / f"claude-ai-career-roadmap-skill-{VERSION}.zip", claude_entries)

    skill_root = ROOT / "skills/generate-ai-career-roadmap"
    skill_entries = [
        (path, f"generate-ai-career-roadmap/{path.relative_to(skill_root).as_posix()}")
        for path in skill_root.rglob("*") if path.is_file()
    ]
    write_zip(OUT / f"generate-ai-career-roadmap-{VERSION}.zip", skill_entries)

    coze_entries = [
        (path, path.relative_to(skill_root).as_posix())
        for path in skill_root.rglob("*")
        if path.is_file() and "agents" not in path.relative_to(skill_root).parts
    ]
    write_zip(OUT / f"coze-generate-ai-career-roadmap-{VERSION}.zip", coze_entries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
