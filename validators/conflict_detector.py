"""Conflict detection logic."""

import logging
from typing import List, Dict, Any, Optional, Set

from data_models.decision import Decision
from data_models.action_item import ActionItem
from data_models.dependency import Dependency

logger = logging.getLogger(__name__)


def _actions_linked_to_decisions(dependencies: List[Dependency]) -> Set[int]:
    """Indices of actions that a dependency connects to a decision (either direction)."""
    linked = set()
    for dep in dependencies:
        ids = (dep.source_id, dep.target_id)
        if not any(i.startswith("Decision ") for i in ids):
            continue
        for identifier in ids:
            if identifier.startswith("Action "):
                try:
                    linked.add(int(identifier.split(" ", 1)[1]))
                except ValueError:
                    pass
    return linked


def detect_conflicts(
    decisions: List[Decision],
    action_items: List[ActionItem],
    dependencies: Optional[List[Dependency]] = None,
) -> Dict[str, Any]:
    """
    Detect conflicts and inconsistencies in decisions and action items.

    Args:
        decisions: List of Decision objects
        action_items: List of ActionItem objects
        dependencies: Decision/action links from the dependency mapper

    Returns:
        Conflict report
    """
    conflicts = []
    linked_actions = _actions_linked_to_decisions(dependencies or [])

    # 1. Detect contradictory decisions
    for i, d1 in enumerate(decisions):
        for j, d2 in enumerate(decisions):
            if i >= j:
                continue

            d1_lower = d1.text.lower()
            d2_lower = d2.text.lower()

            # Check for opposite patterns
            opposite_pairs = [
                ("react", "vue"),
                ("python", "javascript"),
                ("sql", "nosql"),
                ("microservices", "monolith"),
                ("cloud", "on-premise"),
                ("yes", "no"),
                ("will", "will not"),
                ("should", "should not"),
            ]

            for opposite_a, opposite_b in opposite_pairs:
                has_a = opposite_a in d1_lower and opposite_b in d2_lower
                has_b = opposite_b in d1_lower and opposite_a in d2_lower

                if has_a or has_b:
                    conflicts.append({
                        "type": "contradictory_decisions",
                        "decision_a": i,
                        "decision_b": j,
                        "message": f"Decisions {i} and {j} may contradict each other",
                        "decision_a_text": d1.text,
                        "decision_b_text": d2.text,
                    })

    # 2. Check for missing owners on high-priority actions
    for i, action in enumerate(action_items):
        if action.priority == "high" and not action.owner:
            conflicts.append({
                "type": "unowned_critical_task",
                "action_index": i,
                "message": f"High-priority action {i} has no owner",
                "action_text": action.text,
            })

    # 3. Check for circular dependencies (simplified)
    if action_items and decisions:
        for i, action in enumerate(action_items):
            if action.owner:
                owner_lower = action.owner.lower()
                # Check if this action is assigned to everyone/no one clearly
                ambiguous = [
                    "team",
                    "everyone",
                    "people",
                    "we",
                    "they",
                ]
                if owner_lower in ambiguous:
                    conflicts.append({
                        "type": "unclear_responsibility",
                        "action_index": i,
                        "message": f"Action {i} responsibility is unclear",
                        "owner": action.owner,
                    })

    # 4. Check for action items without related decisions
    for i, action in enumerate(action_items):
        if not action.related_decision_id and i not in linked_actions:
            conflicts.append({
                "type": "orphaned_action",
                "action_index": i,
                "message": f"Action {i} is not linked to any decision",
                "action_text": action.text,
            })

    return {
        "conflict_count": len(conflicts),
        "conflicts": conflicts,
        "has_contradictions": any(c["type"] == "contradictory_decisions" for c in conflicts),
        "has_unowned_critical": any(
            c["type"] == "unowned_critical_task" for c in conflicts
        ),
        "summary": f"Detected {len(conflicts)} potential conflict(s)",
    }
