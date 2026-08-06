.PHONY: verify paper checksums

verify:
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/replay_all.py

paper:
	tectonic manuscript/a286874_bounds.tex

checksums:
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_sha256s.py
