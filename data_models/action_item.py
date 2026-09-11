"""Action item data model."""

from pydantic import BaseModel, Field
from typing import Optional


class ActionItem(BaseModel):
    """Extracted action item from a meeting."""

    text: str = Field(..., description="The action item text")
    owner: Optional[str] = Field(None, description="Person responsible")
    deadline: Optional[str] = Field(None, description="Due date or deadline")
    priority: str = Field(default="medium", description="low, medium, or high")
    status: str = Field(default="open", description="open, in_progress, or completed")
    evidence_text: str = Field(..., description="Full text excerpt from transcript")
    related_decision_id: Optional[str] = Field(None, description="ID of related decision")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "text": "Setup the React development environment",
                "owner": "Frontend Developer",
                "deadline": "2024-08-31",
                "priority": "high",
                "status": "open",
                "evidence_text": "John, can you setup the React dev environment by Friday?",
                "related_decision_id": "dec_001",
            }
        }
