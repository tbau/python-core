"""Path utility functions with explicit safety boundaries.

Use these when file paths come from configuration or user input. The safe-join
helpers resolve paths first so ``..`` segments cannot silently escape a root.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import tempfile


def ensure_directory(path: str | Path) -> Path:
    """Create a directory and return its resolved absolute path."""

    directory = Path(path).expanduser().resolve()
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def is_within_directory(path: str | Path, root: str | Path) -> bool:
    """Return whether a path resolves inside a root directory."""

    resolved_root = Path(root).expanduser().resolve()
    resolved_path = Path(path).expanduser().resolve()
    return resolved_path == resolved_root or resolved_path.is_relative_to(resolved_root)


def safe_join(root: str | Path, *parts: str | Path) -> Path:
    """Join path parts and ensure the result stays under root."""

    resolved_root = Path(root).expanduser().resolve()
    candidate = resolved_root.joinpath(*parts).resolve()
    if not (candidate == resolved_root or candidate.is_relative_to(resolved_root)):
        raise ValueError(f"path escapes root: {candidate}")
    return candidate


def sanitize_filename(value: str, *, replacement: str = "_") -> str:
    """Return a filename-safe string for common operating systems."""

    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', replacement, value).strip()
    cleaned = re.sub(f"{re.escape(replacement)}+", replacement, cleaned)
    return cleaned.strip(". ") or "untitled"


def file_sha256(path: str | Path, *, chunk_size: int = 1024 * 1024) -> str:
    """Return SHA-256 hex digest for a file without loading it all at once."""

    digest = hashlib.sha256()
    with Path(path).open("rb") as file_handle:
        while chunk := file_handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def write_text_atomic(path: str | Path, text: str, *, encoding: str = "utf-8") -> Path:
    """Write text via a temporary file and atomic replace.

    This reduces the chance that a crash leaves a partially written target file.
    """

    target = Path(path).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.", text=True)
    try:
        with os.fdopen(descriptor, "w", encoding=encoding) as file_handle:
            file_handle.write(text)
        Path(temp_name).replace(target)
    except Exception:
        Path(temp_name).unlink(missing_ok=True)
        raise
    return target
