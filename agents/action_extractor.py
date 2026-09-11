"""Action item extraction agent using Gemini."""

import logging
import json
from typing import List
from agents.gemini_client import generate_json_text
from data_models.action_item import ActionItem

logger = logging.getLogger(__name__)


def extract_action_items(transcript_text: str) -> List[ActionItem]:
    """
    Extract action items from a meeting transcript using Gemini with fallback.

    Args:
        transcript_text: Full meeting transcript

    Returns:
        List of ActionItem objects
    """
    try:
        prompt = """Extract action items from this meeting transcript.

For each action item, identify: text, owner (or null), deadline (or null), priority (high/medium/low).

Return ONLY valid JSON - no markdown, no extra text:
{"action_items": [{"text": "...", "owner": "...", "deadline": "...", "priority": "high", "evidence_text": "...", "confidence": 0.85}]}

Meeting Transcript:
""" + transcript_text + "\n\nReturn only JSON:"

        result = json.loads(generate_json_text(prompt))

        action_items = []
        for item_data in result.get("action_items", []):
            action_item = ActionItem(
                text=item_data.get("text", ""),
                owner=item_data.get("owner"),
                deadline=item_data.get("deadline"),
                priority=item_data.get("priority", "medium"),
                status="open",
                evidence_text=item_data.get("evidence_text", ""),
            )
            action_items.append(action_item)

        logger.info(f"Extracted {len(action_items)} action items from transcript")
        return action_items

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response as JSON: {e}")
        return []
