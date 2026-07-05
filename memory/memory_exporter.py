from __future__ import annotations

from pathlib import Path

from .brain_manager import BrainManager


class MemoryExporter:
    def __init__(self, brain_manager: BrainManager) -> None:
        self.brain_manager = brain_manager

    def export_markdown(self, path: Path) -> None:
        self.brain_manager.export_brain(path)
