"""Decision extraction agent using Gemini."""

import logging
import json
from typing import List
from datetime import datetime

from agents.gemini_client import generate_json_text
from data_models.decision import Decision

logger = logging.getLogger(__name__)


def extract_decisions(transcript_text: str) -> List[Decision]:
    """
    Extract decisions from a meeting transcript using Gemini with fallback.

    Args:
        transcript_text: Full meeting transcript

    Returns:
        List of Decision objects
    """
    try:
        prompt = """Extract key decisions from this meeting transcript.

For each decision, identify: text, confidence (0-1.0), evidence_text (exact quote), evidence_speaker (or null), evidence_timestamp (or null).

Return ONLY valid JSON - no markdown:
{"decisions": [{"text": "...", "confidence": 0.9, "evidence_text": "...", "evidence_speaker": "...", "evidence_timestamp": "..."}]}

Meeting Transcript:
""" + transcript_text + "\n\nReturn only JSON:"

        result = json.loads(generate_json_text(prompt))

        decisions = []
        for decision_data in result.get("decisions", []):
            decision = Decision(
                text=decision_data.get("text", ""),
                confidence=float(decision_data.get("confidence", 0.5)),
                evidence_speaker=decision_data.get("evidence_speaker"),
                evidence_timestamp=decision_data.get("evidence_timestamp"),
                evidence_text=decision_data.get("evidence_text", ""),
                extracted_at=datetime.now().isoformat(),
            )
            decisions.append(decision)

        logger.info(f"Extracted {len(decisions)} decisions from transcript")
        return decisions

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response as JSON: {e}")
        return []
