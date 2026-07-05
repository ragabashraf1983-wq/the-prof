"""Compatibility package for the flat source-tree layout.

The repository stores source folders such as ``app/``, ``core/`` and
``providers/`` at the project root.  Runtime imports use the package name
``the_prof``.  Extending ``__path__`` to include the repository root lets
``import the_prof.app`` resolve to ``<repo>/app`` without duplicating files.
"""

from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_repo_root_str = str(_REPO_ROOT)
if _repo_root_str not in __path__:
    __path__.append(_repo_root_str)
