from __future__ import annotations

from pathlib import Path

from .brain_manager import BrainManager


class MemoryImporter:
    def __init__(self, brain_manager: BrainManager) -> None:
        self.brain_manager = brain_manager

    def import_markdown(self, path: Path) -> dict[str, int]:
        return self.brain_manager.import_brain(path)
