from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .models import utc_now_iso


@dataclass(slots=True)
class AuditEvent:
    timestamp: str
    level: str
    message: str


class AuditLog:
    def __init__(self, log_path: Path) -> None:
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.write_text("# The Prof Log\n\n", encoding="utf-8")

    def write(self, level: str, message: str) -> None:
        event = f"- [{utc_now_iso()}] **{level.upper()}** {message}\n"
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(event)

    def info(self, message: str) -> None:
        self.write("info", message)

    def warning(self, message: str) -> None:
        self.write("warning", message)

    def error(self, message: str) -> None:
        self.write("error", message)
