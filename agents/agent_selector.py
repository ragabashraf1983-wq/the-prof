from __future__ import annotations

from the_prof.core.models import ProjectIntake


class AgentSelector:
    def select(self, intake: ProjectIntake) -> list[str]:
        common = [
            "Principal Investigator Agent",
            "Project Manager Agent",
            "Ethical Review Board Agent",
            "Prior Art Detective Agent",
            "Markdown Typesetter Agent",
            "BibTeX Librarian Agent",
        ]
        if intake.scope == "Gap Analysis":
            return common + [
                "Blue-Sky Visionary Agent",
                "Devil’s Advocate Agent",
                "Reviewer 2: Supportive Skeptic",
                "Reviewer 3: Career Destroyer",
            ]
        if intake.scope in {"Research Proposal", "Grant Proposal", "Pilot Study Paper"}:
            return common + [
                "Experimental Architect Agent",
                "Discussion & Future Work Philosopher Agent",
                "Abstract & Hook Agent",
                "Reviewer 1: Pedantic Typo Hunter",
                "Reviewer 2: Supportive Skeptic",
            ]
        if intake.scope in {"Literature Review", "Review Paper", "Scoping Review Plan", "Systematic Review Plan"}:
            return common + [
                "Data Scavenger Agent",
                "Discussion & Future Work Philosopher Agent",
                "Reviewer 1: Pedantic Typo Hunter",
                "Reviewer 2: Supportive Skeptic",
            ]
        return common + [
            "Abstract & Hook Agent",
            "Methods & Materials Chronographer Agent",
            "Discussion & Future Work Philosopher Agent",
            "Reviewer 1: Pedantic Typo Hunter",
        ]
