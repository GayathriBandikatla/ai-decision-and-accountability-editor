"""Decision data model."""

from pydantic import BaseModel, Field
from typing import Optional


class Decision(BaseModel):
    """Extracted decision from a meeting."""

    text: str = Field(..., description="The decision text")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score 0-1")
    evidence_timestamp: Optional[str] = Field(None, description="Timestamp in transcript")
    evidence_speaker: Optional[str] = Field(None, description="Speaker name")
    evidence_text: str = Field(..., description="Full text excerpt from transcript")
    extracted_at: Optional[str] = Field(None, description="ISO timestamp when extracted")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "text": "We will use React for the frontend",
                "confidence": 0.95,
                "evidence_timestamp": "00:05:30",
                "evidence_speaker": "Tech Lead",
                "evidence_text": "Let's go with React for the frontend. It has good support and the team is familiar with it.",
                "extracted_at": "2024-08-26T10:00:00Z",
            }
        }
