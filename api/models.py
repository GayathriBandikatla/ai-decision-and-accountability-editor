"""Pydantic models for API requests and responses."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from data_models.decision import Decision
from data_models.action_item import ActionItem
from data_models.dependency import Dependency


class AnalyzeRequest(BaseModel):
    """Request body for /analyze endpoint."""

    transcript_text: str = Field(..., description="Full meeting transcript")

    class Config:
        json_schema_extra = {
            "example": {
                "transcript_text": "Team lead: Let's discuss the project timeline. Developer: When should we start? Team lead: Next week. We'll use React for frontend and Python for backend..."
            }
        }


class AnalyzeResponse(BaseModel):
    """Response from /analyze endpoint."""

    decisions: List[Decision]
    action_items: List[ActionItem]
    dependencies: List[Dependency]
    validation: Dict[str, Any]
    conflicts: Dict[str, Any]
    stats: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "decisions": [
                    {
                        "text": "We will use React for the frontend",
                        "confidence": 0.95,
                        "evidence_timestamp": "00:05:30",
                        "evidence_speaker": "Tech Lead",
                        "evidence_text": "...",
                        "extracted_at": "2024-08-26T10:00:00",
                    }
                ],
                "action_items": [
                    {
                        "text": "Setup React development environment",
                        "owner": "Frontend Developer",
                        "deadline": "2024-08-31",
                        "priority": "high",
                        "status": "open",
                        "evidence_text": "...",
                        "related_decision_id": "dec_1",
                    }
                ],
                "dependencies": [
                    {
                        "source_id": "dec_1",
                        "target_id": "action_1",
                        "relationship": "enables",
                        "confidence": 0.85,
                    }
                ],
                "validation": {
                    "decision_count": 5,
                    "issues": [],
                    "summary": "...",
                },
                "conflicts": {
                    "conflict_count": 0,
                    "conflicts": [],
                    "summary": "...",
                },
                "stats": {
                    "decision_count": 5,
                    "action_count": 3,
                    "owner_count": 2,
                },
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    message: str
