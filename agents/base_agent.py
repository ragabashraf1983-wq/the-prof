from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True)
class AgentSkill:
    name: str
    role: str
    bounded_task: str
    skill_file: Path
    hallucination_control_rules: list[str]
    permitted_actions: list[str]
    prohibited_actions: list[str]
    input_schema: list[str]
    output_schema: list[str]
    review_requirements: list[str]

    @classmethod
    def from_file(cls, path: Path) -> "AgentSkill":
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return cls(
            name=data["name"],
            role=data["role"],
            bounded_task=data["bounded_task"],
            skill_file=path,
            hallucination_control_rules=data.get("hallucination_control_rules", []),
            permitted_actions=data.get("permitted_actions", []),
            prohibited_actions=data.get("prohibited_actions", []),
            input_schema=data.get("input_schema", []),
            output_schema=data.get("output_schema", []),
            review_requirements=data.get("review_requirements", []),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "bounded_task": self.bounded_task,
            "skill_file": str(self.skill_file),
            "hallucination_control_rules": self.hallucination_control_rules,
            "permitted_actions": self.permitted_actions,
            "prohibited_actions": self.prohibited_actions,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "review_requirements": self.review_requirements,
        }
