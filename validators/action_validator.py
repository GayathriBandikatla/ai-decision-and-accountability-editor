"""Action item validation logic."""

import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta

from data_models.action_item import ActionItem

logger = logging.getLogger(__name__)


def validate_actions(action_items: List[ActionItem]) -> Dict[str, Any]:
    """
    Validate extracted action items using deterministic rules.

    Args:
        action_items: List of ActionItem objects

    Returns:
        Validation report with issues
    """
    issues = []

    if not action_items:
        logger.warning("No action items to validate")
        return {
            "action_count": 0,
            "issues": [],
            "issue_count": 0,
            "owned_actions": 0,
            "high_priority_count": 0,
            "summary": "No action items extracted",
        }

    ambiguous_owners = [
        "team",
        "someone",
        "everyone",
        "people",
        "we",
        "they",
        "group",
        "all",
        "folks",
    ]

    for i, action in enumerate(action_items):
        # 1. Check for missing owner
        if not action.owner:
            issues.append({
                "type": "missing_owner",
                "action_index": i,
                "message": f"Action {i} has no assigned owner: '{action.text}'",
            })
        elif action.owner.lower() in ambiguous_owners:
            issues.append({
                "type": "ambiguous_owner",
                "action_index": i,
                "message": f"Action {i} has ambiguous owner: '{action.owner}' (should be specific person)",
            })

        # 2. Check for missing deadline
        if not action.deadline:
            if action.priority == "high":
                issues.append({
                    "type": "missing_deadline",
                    "action_index": i,
                    "message": f"High-priority action {i} has no deadline",
                })

        # 3. Check for unrealistic deadlines
        if action.deadline:
            try:
                deadline = datetime.fromisoformat(action.deadline.split("T")[0])
                now = datetime.now()

                # Past deadline
                if deadline < now:
                    issues.append({
                        "type": "past_deadline",
                        "action_index": i,
                        "message": f"Action {i} deadline is in the past: {action.deadline}",
                    })

                # Too far in future (> 1 year)
                if deadline > now + timedelta(days=365):
                    issues.append({
                        "type": "unrealistic_deadline",
                        "action_index": i,
                        "message": f"Action {i} deadline is too far in future: {action.deadline}",
                    })
            except (ValueError, AttributeError):
                # Invalid date format
                pass

        # 4. Check for very vague action text
        if len(action.text.split()) < 3:
            issues.append({
                "type": "vague_action",
                "action_index": i,
                "message": f"Action {i} is too vague: '{action.text}'",
            })

        # 5. Check for missing evidence
        if not action.evidence_text or len(action.evidence_text.strip()) < 10:
            issues.append({
                "type": "missing_evidence",
                "action_index": i,
                "message": f"Action {i} has no or minimal evidence",
            })

    # 6. Check for duplicate action items
    for i, a1 in enumerate(action_items):
        for j, a2 in enumerate(action_items):
            if i >= j:
                continue
            if a1.text.lower() == a2.text.lower():
                issues.append({
                    "type": "duplicate_action",
                    "action_index": i,
                    "message": f"Actions {i} and {j} are identical",
                })

    return {
        "action_count": len(action_items),
        "issues": issues,
        "issue_count": len(issues),
        "owned_actions": sum(1 for a in action_items if a.owner),
        "high_priority_count": sum(1 for a in action_items if a.priority == "high"),
        "summary": f"Validated {len(action_items)} actions with {len(issues)} issue(s)",
    }
