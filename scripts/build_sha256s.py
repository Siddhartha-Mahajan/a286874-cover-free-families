#!/usr/bin/env python3
"""Write SHA256SUMS for every package file except SHA256SUMS itself."""

from __future__ import annotations

from common import PACKAGE, sha256


def main() -> None:
    excluded = {PACKAGE / "SHA256SUMS"}
    files = sorted(
        path
        for path in PACKAGE.rglob("*")
        if path.is_file()
        and path not in excluded
        and ".git" not in path.parts
        and "__pycache__" not in path.parts
        and not path.name.endswith(".pyc")
    )
    lines = [f"{sha256(path)}  {path.relative_to(PACKAGE).as_posix()}" for path in files]
    (PACKAGE / "SHA256SUMS").write_text("\n".join(lines) + "\n")
    print(f"wrote {len(lines)} checksums")


if __name__ == "__main__":
    main()
