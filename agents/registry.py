from __future__ import annotations

from pathlib import Path

from .base_agent import AgentSkill


class AgentRegistry:
    def __init__(self, skill_dir: Path) -> None:
        if not skill_dir.exists() and len(skill_dir.parts) >= 3 and skill_dir.parts[-3:] == ("the_prof", "agents", "skills"):
            flat_skill_dir = skill_dir.parents[2] / "agents" / "skills"
            if flat_skill_dir.exists():
                skill_dir = flat_skill_dir
        self.skill_dir = skill_dir
        self.skills = self._load_skills()

    def _load_skills(self) -> dict[str, AgentSkill]:
        skills: dict[str, AgentSkill] = {}
        for path in sorted(self.skill_dir.glob("*.yaml")):
            skill = AgentSkill.from_file(path)
            skills[skill.name] = skill
        return skills

    def list_skills(self) -> list[AgentSkill]:
        return list(self.skills.values())

    def get(self, name: str) -> AgentSkill:
        return self.skills[name]
