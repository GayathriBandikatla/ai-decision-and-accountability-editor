"""Tests for validator modules."""

import pytest
from data_models.decision import Decision
from data_models.action_item import ActionItem
from data_models.dependency import Dependency
from validators.decision_validator import validate_decisions
from validators.action_validator import validate_actions
from validators.conflict_detector import detect_conflicts


class TestDecisionValidator:
    """Tests for decision validation."""

    def test_validate_empty_decisions(self):
        """Test validation with no decisions."""
        result = validate_decisions([])
        assert result['decision_count'] == 0
        assert result['issue_count'] == 0
        assert len(result['issues']) == 0

    def test_validate_single_decision(self):
        """Test validation with a single decision."""
        decision = Decision(
            text="We will use React",
            confidence=0.95,
            evidence_speaker="Team lead",
            evidence_text="Team lead said we'll use React for frontend"
        )
        result = validate_decisions([decision])
        assert result['decision_count'] == 1
        assert result['issue_count'] == 0

    def test_duplicate_detection(self):
        """Test detection of duplicate decisions."""
        decision1 = Decision(
            text="We will use React",
            confidence=0.95,
            evidence_text="Team lead said we'll use React"
        )
        decision2 = Decision(
            text="We will use React",
            confidence=0.90,
            evidence_text="Confirmed by developer"
        )
        result = validate_decisions([decision1, decision2])
        assert result['issue_count'] > 0
        assert any(issue['type'] == 'duplicate' for issue in result['issues'])

    def test_low_confidence_flag(self):
        """Test flagging of low confidence decisions."""
        decision = Decision(
            text="Maybe we should consider React",
            confidence=0.45,
            evidence_text="Someone mentioned React"
        )
        result = validate_decisions([decision])
        assert any(issue['type'] == 'low_confidence' for issue in result['issues'])

    def test_missing_evidence(self):
        """Test detection of missing evidence."""
        decision = Decision(
            text="Use React",
            confidence=0.8,
            evidence_text=""
        )
        result = validate_decisions([decision])
        assert any(issue['type'] == 'missing_evidence' for issue in result['issues'])

    def test_vague_decision(self):
        """Test detection of vague decisions."""
        decision = Decision(
            text="OK",
            confidence=0.5,
            evidence_text="Someone said OK"
        )
        result = validate_decisions([decision])
        assert any(issue['type'] == 'vague_decision' for issue in result['issues'])

    def test_confidence_average(self):
        """Test calculation of average confidence."""
        decisions = [
            Decision(
                text="Decision 1",
                confidence=0.9,
                evidence_text="Evidence 1"
            ),
            Decision(
                text="Decision 2",
                confidence=0.8,
                evidence_text="Evidence 2"
            ),
        ]
        result = validate_decisions(decisions)
        assert result['confidence_average'] == 0.85


class TestActionValidator:
    """Tests for action item validation."""

    def test_validate_empty_actions(self):
        """Test validation with no action items."""
        result = validate_actions([])
        assert result['action_count'] == 0
        assert result['issue_count'] == 0

    def test_missing_owner(self):
        """Test detection of missing owner."""
        action = ActionItem(
            text="Setup dev environment",
            owner=None,
            evidence_text="Someone should setup the dev environment"
        )
        result = validate_actions([action])
        assert any(issue['type'] == 'missing_owner' for issue in result['issues'])

    def test_ambiguous_owner(self):
        """Test detection of ambiguous owner."""
        action = ActionItem(
            text="Setup dev environment",
            owner="team",
            evidence_text="Team should setup dev environment"
        )
        result = validate_actions([action])
        assert any(issue['type'] == 'ambiguous_owner' for issue in result['issues'])

    def test_high_priority_missing_deadline(self):
        """Test high priority action without deadline."""
        action = ActionItem(
            text="Fix critical bug",
            owner="John",
            priority="high",
            deadline=None,
            evidence_text="Critical bug needs fixing"
        )
        result = validate_actions([action])
        assert any(issue['type'] == 'missing_deadline' for issue in result['issues'])

    def test_valid_action_item(self):
        """Test validation of valid action item."""
        action = ActionItem(
            text="Setup React development environment",
            owner="Frontend Developer",
            priority="high",
            deadline="2024-08-31",
            evidence_text="John will setup the React dev environment by Friday"
        )
        result = validate_actions([action])
        assert result['action_count'] == 1
        assert any(issue['type'] != 'vague_action' for issue in result['issues'])

    def test_owned_actions_count(self):
        """Test counting of owned actions."""
        actions = [
            ActionItem(
                text="Action 1",
                owner="Person 1",
                evidence_text="Evidence 1"
            ),
            ActionItem(
                text="Action 2",
                owner=None,
                evidence_text="Evidence 2"
            ),
            ActionItem(
                text="Action 3",
                owner="Person 3",
                evidence_text="Evidence 3"
            ),
        ]
        result = validate_actions(actions)
        assert result['owned_actions'] == 2


class TestConflictDetector:
    """Tests for conflict detection."""

    def test_no_conflicts(self):
        """Test when there are no conflicts."""
        decisions = [
            Decision(
                text="Use React",
                confidence=0.9,
                evidence_text="Use React for frontend"
            ),
            Decision(
                text="Use Python for backend",
                confidence=0.9,
                evidence_text="Python for backend"
            ),
        ]
        conflicts = detect_conflicts(decisions, [])
        assert conflicts['conflict_count'] == 0

    def test_contradictory_decisions(self):
        """Test detection of contradictory decisions."""
        decisions = [
            Decision(
                text="Use React for frontend",
                confidence=0.9,
                evidence_text="React is better"
            ),
            Decision(
                text="Use Vue for frontend",
                confidence=0.8,
                evidence_text="Vue is also good"
            ),
        ]
        conflicts = detect_conflicts(decisions, [])
        assert conflicts['has_contradictions'] is True

    def test_unowned_critical_task(self):
        """Test detection of unowned critical tasks."""
        actions = [
            ActionItem(
                text="Fix critical security bug",
                owner=None,
                priority="high",
                evidence_text="Security issue found"
            ),
        ]
        conflicts = detect_conflicts([], actions)
        assert conflicts['has_unowned_critical'] is True

    def test_ambiguous_responsibility(self):
        """Test detection of ambiguous responsibility."""
        actions = [
            ActionItem(
                text="Complete project",
                owner="team",
                evidence_text="Team should complete the project"
            ),
        ]
        conflicts = detect_conflicts([], actions)
        assert conflicts['conflict_count'] > 0

    def test_orphaned_action_without_dependencies(self):
        """An action with no decision link is reported as orphaned."""
        decisions = [Decision(text="Use React", confidence=0.9, evidence_text="Use React for UI")]
        actions = [ActionItem(text="Setup React project", owner="Alice", evidence_text="Alice sets up React")]
        conflicts = detect_conflicts(decisions, actions)
        assert any(c['type'] == 'orphaned_action' for c in conflicts['conflicts'])

    def test_action_linked_via_dependency_is_not_orphaned(self):
        """Dependency mapper links count as decision links."""
        decisions = [Decision(text="Use React", confidence=0.9, evidence_text="Use React for UI")]
        actions = [
            ActionItem(text="Setup React project", owner="Alice", evidence_text="Alice sets up React"),
            ActionItem(text="Write docs", owner="Bob", evidence_text="Bob writes docs"),
        ]
        dependencies = [
            Dependency(source_id="Decision 0", target_id="Action 0", relationship="enables", confidence=0.9),
            Dependency(source_id="Action 0", target_id="Action 1", relationship="blocks", confidence=0.8),
        ]
        conflicts = detect_conflicts(decisions, actions, dependencies)
        orphaned = [c['action_index'] for c in conflicts['conflicts'] if c['type'] == 'orphaned_action']
        assert orphaned == [1]


class TestValidatorIntegration:
    """Integration tests for validators."""

    def test_full_validation_pipeline(self):
        """Test running all validators together."""
        decisions = [
            Decision(
                text="Use React for frontend",
                confidence=0.9,
                evidence_text="Team lead decided to use React"
            ),
            Decision(
                text="Use React",
                confidence=0.85,
                evidence_text="Confirmed: we'll use React"
            ),
        ]

        actions = [
            ActionItem(
                text="Setup React development environment",
                owner="Frontend Dev",
                priority="high",
                deadline="2024-08-31",
                evidence_text="John will setup React env by Friday"
            ),
        ]

        decision_result = validate_decisions(decisions)
        action_result = validate_actions(actions)
        conflict_result = detect_conflicts(decisions, actions)

        assert decision_result['decision_count'] == 2
        assert action_result['action_count'] == 1
        assert conflict_result['conflict_count'] >= 1  # Duplicate decisions


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
