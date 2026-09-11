"""Dependency mapping agent using Gemini."""

import logging
import json
from typing import List

from agents.gemini_client import generate_json_text
from data_models.dependency import Dependency
from data_models.decision import Decision
from data_models.action_item import ActionItem

logger = logging.getLogger(__name__)


def extract_dependencies(
    transcript_text: str,
    decisions: List[Decision],
    action_items: List[ActionItem],
) -> List[Dependency]:
    """
    Extract dependencies between decisions and action items using Gemini.

    Args:
        transcript_text: Full meeting transcript
        decisions: List of extracted decisions
        action_items: List of extracted action items

    Returns:
        List of Dependency objects
    """
    try:
        if not decisions and not action_items:
            logger.warning("No decisions or actions to map dependencies")
            return []

        # Format decisions and actions for the prompt
        decisions_str = "\n".join(
            [f"Decision {i}: {d.text}" for i, d in enumerate(decisions)]
        )
        actions_str = "\n".join(
            [f"Action {i}: {a.text}" for i, a in enumerate(action_items)]
        )

        prompt = f"""Analyze the relationships between these decisions and action items from the meeting.

Decisions:
{decisions_str}

Action Items:
{actions_str}

For each relationship, identify:
1. Which decision or action it comes from (source)
2. Which decision or action it relates to (target)
3. Relationship type: "blocks", "depends_on", "conflicts_with", "enables"
4. Confidence score (0.0-1.0)

Return as valid JSON only:
{{
  "dependencies": [
    {{
      "source_id": "Decision 0 or Action 1",
      "target_id": "Decision 1 or Action 2",
      "relationship": "blocks",
      "confidence": 0.85
    }}
  ]
}}

IMPORTANT:
- Return ONLY valid JSON, no markdown
- Use exact format: "Decision N" or "Action N"
- Relationship types: blocks, depends_on, conflicts_with, enables
- Only include clear, confident relationships
- Confidence: 0.8-1.0 for obvious, 0.6-0.8 for probable

Return only the JSON object:"""

        result = json.loads(generate_json_text(prompt))

        dependencies = []
        for dep_data in result.get("dependencies", []):
            dependency = Dependency(
                source_id=dep_data.get("source_id", ""),
                target_id=dep_data.get("target_id", ""),
                relationship=dep_data.get("relationship", "depends_on"),
                confidence=float(dep_data.get("confidence", 0.5)),
            )
            dependencies.append(dependency)

        logger.info(f"Extracted {len(dependencies)} dependencies")
        return dependencies

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response as JSON: {e}")
        return []
