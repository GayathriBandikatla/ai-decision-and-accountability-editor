"""Decision validation logic."""

import logging
from typing import List, Dict, Any
from difflib import SequenceMatcher

from data_models.decision import Decision

logger = logging.getLogger(__name__)


class ValidationIssue:
    """Single validation issue."""

    def __init__(self, issue_type: str, message: str, decision_index: int = None):
        self.type = issue_type
        self.message = message
        self.decision_index = decision_index

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "message": self.message,
            "decision_index": self.decision_index,
        }


def similarity_ratio(a: str, b: str) -> float:
    """Calculate similarity between two strings (0.0 to 1.0)."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def validate_decisions(decisions: List[Decision]) -> Dict[str, Any]:
    """
    Validate extracted decisions using deterministic rules.

    Args:
        decisions: List of Decision objects

    Returns:
        Validation report with issues and metadata
    """
    issues = []

    if not decisions:
        logger.warning("No decisions to validate")
        return {
            "decision_count": 0,
            "issues": [],
            "issue_count": 0,
            "confidence_average": 0,
            "summary": "No decisions extracted",
        }

    # 1. Check for duplicates (fuzzy match)
    for i, d1 in enumerate(decisions):
        for j, d2 in enumerate(decisions):
            if i >= j:
                continue

            similarity = similarity_ratio(d1.text, d2.text)
            if similarity > 0.8:
                issues.append(
                    ValidationIssue(
                        issue_type="duplicate",
                        message=f"Decision {i} and {j} are very similar (similarity: {similarity:.2%})",
                        decision_index=i,
                    )
                )

    # 2. Check confidence levels
    for i, decision in enumerate(decisions):
        if decision.confidence < 0.6:
            issues.append(
                ValidationIssue(
                    issue_type="low_confidence",
                    message=f"Decision {i} has low confidence: {decision.confidence:.0%}",
                    decision_index=i,
                )
            )

    # 3. Check for missing evidence
    for i, decision in enumerate(decisions):
        if not decision.evidence_text or len(decision.evidence_text.strip()) < 10:
            issues.append(
                ValidationIssue(
                    issue_type="missing_evidence",
                    message=f"Decision {i} has no or minimal evidence",
                    decision_index=i,
                )
            )

    # 4. Check for missing speaker
    for i, decision in enumerate(decisions):
        if not decision.evidence_speaker:
            issues.append(
                ValidationIssue(
                    issue_type="missing_speaker",
                    message=f"Decision {i} does not link to a speaker",
                    decision_index=i,
                )
            )

    # 5. Check for very short decision text
    for i, decision in enumerate(decisions):
        if len(decision.text.split()) < 3:
            issues.append(
                ValidationIssue(
                    issue_type="vague_decision",
                    message=f"Decision {i} is too vague or short: '{decision.text}'",
                    decision_index=i,
                )
            )

    return {
        "decision_count": len(decisions),
        "issues": [issue.to_dict() for issue in issues],
        "issue_count": len(issues),
        "confidence_average": round(
            sum(d.confidence for d in decisions) / len(decisions), 3
        ),
        "summary": f"Validated {len(decisions)} decisions with {len(issues)} issue(s)",
    }
