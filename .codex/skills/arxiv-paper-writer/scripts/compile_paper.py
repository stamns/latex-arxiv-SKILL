#!/usr/bin/env python3
"""Compile main.tex for a paper project."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from paper_utils import check_latex_available


def run(cmd: list[str], cwd: Path) -> int:
    result = subprocess.run(cmd, cwd=str(cwd))
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile main.tex (pdflatex/bibtex or latexmk).")
    parser.add_argument(
        "--project-dir",
        default=".",
        help="Project directory containing main.tex and ref.bib.",
    )
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    tex_path = project_dir / "main.tex"

    if not tex_path.exists():
        print(f"error: main.tex not found in {project_dir}", file=sys.stderr)
        return 1

    latex_info = check_latex_available()
    if not latex_info["available"]:
        print("error: LaTeX tools not available (pdflatex + bibtex required).", file=sys.stderr)
        return 1

    latexmk = latex_info.get("latexmk")
    if latexmk:
        cmd = [
            latexmk,
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "main.tex",
        ]
        return run(cmd, project_dir)

    # Fallback: pdflatex + bibtex
    steps = [
        [latex_info["pdflatex"], "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        [latex_info["bibtex"], "main"],
        [latex_info["pdflatex"], "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        [latex_info["pdflatex"], "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
    ]

    for cmd in steps:
        code = run(cmd, project_dir)
        if code != 0:
            return code

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
