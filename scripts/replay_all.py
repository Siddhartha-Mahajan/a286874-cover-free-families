#!/usr/bin/env python3
"""One-command replay of every claimed result in this final package."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from common import PACKAGE, sha256, write_json


def run(script: str) -> None:
    subprocess.run(
        [sys.executable, str(PACKAGE / "scripts" / script)],
        cwd=PACKAGE,
        check=True,
    )


def load(name: str) -> dict:
    return json.loads((PACKAGE / "certificates" / name).read_text())


def main() -> None:
    run("certify_a15_exact.py")
    run("certify_a16_upper.py")
    run("certify_a17_exact.py")

    a15 = load("a15_exact.json")
    a16 = load("a16_upper_54.json")
    a17 = load("a17_exact.json")
    if not a15["proved"] or a15["claim"] != "A286874(15)=42":
        raise AssertionError("a(15) replay summary failed")
    if not a16["proved"] or not a16["proves_no_55_member_family"]:
        raise AssertionError("a(16) replay summary failed")
    if not a17["proved"] or a17["claim"] != "A286874(17)=68":
        raise AssertionError("a(17) replay summary failed")

    immutable_inputs = [
        PACKAGE / "sources/a14_extremals_A303977.txt",
        PACKAGE / "constructions/a15_42.txt",
        PACKAGE / "constructions/a16_48.txt",
        PACKAGE / "constructions/a17_68.txt",
    ]
    summary = {
        "package_claims": {
            "A286874(15)": 42,
            "A286874(16)": {"lower": 48, "upper": 54},
            "A286874(17)": 68,
        },
        "all_certificates_passed": True,
        "certificate_files": [
            "certificates/a15_exact.json",
            "certificates/a16_upper_54.json",
            "certificates/a17_exact.json",
        ],
        "immutable_input_sha256": {
            str(path.relative_to(PACKAGE)): sha256(path) for path in immutable_inputs
        },
        "runtime_dependency": "Python standard library only",
    }
    write_json(PACKAGE / "certificates/replay_summary.json", summary)
    print("all final A286874 certificates passed")


if __name__ == "__main__":
    main()
