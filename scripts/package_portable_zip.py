from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)
OUT = DIST / "the-prof-portable.zip"

INCLUDE_PATHS = [
    "main.py",
    "requirements.txt",
    "README.md",
    "DEVSTATE.md",
    "start_the_prof.bat",
    "build_windows_zip.bat",
    "build_windows_exe.bat",
    "TheProf_logo.png",
    "the_prof",
    "docs",
    "brain",
    "scripts",
]

EXCLUDE_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "dist",
    "build",
    "coverage",
    "node_modules",
    "target",
    "out",
}

EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".log"}


def should_include(path: Path) -> bool:
    if any(part in EXCLUDE_PARTS for part in path.parts):
        return False
    if path.suffix.lower() in EXCLUDE_SUFFIXES:
        return False
    return True


def iter_files(base: Path):
    if base.is_file():
        yield base
        return
    for path in base.rglob("*"):
        if path.is_file() and should_include(path):
            yield path


def main() -> None:
    with ZipFile(OUT, "w", compression=ZIP_DEFLATED) as archive:
        for rel in INCLUDE_PATHS:
            path = ROOT / rel
            if not path.exists():
                continue
            for file_path in iter_files(path):
                archive.write(file_path, file_path.relative_to(ROOT))
    print(f"Created {OUT}")


if __name__ == "__main__":
    main()
