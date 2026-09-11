"""FastAPI application setup."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.api_core.exceptions import ResourceExhausted
import logging

from config.settings import settings
from api.models import AnalyzeRequest, AnalyzeResponse, HealthResponse
from api.cache import analysis_cache
from agents import extract_decisions, extract_action_items, extract_dependencies
from validators import validate_decisions, validate_actions, detect_conflicts

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Patchamomma API",
    description="AI Decision & Accountability Auditor",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="Patchamomma API is running",
    )


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    """
    Analyze a meeting transcript and extract decisions, actions, and dependencies.

    Args:
        request: AnalyzeRequest with transcript_text

    Returns:
        AnalyzeResponse with extracted data and validation results
    """
    try:
        if not request.transcript_text or len(request.transcript_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Transcript must be at least 50 characters long",
            )

        # Check cache first
        cached_result = analysis_cache.get(request.transcript_text)
        if cached_result:
            logger.info("Returning cached analysis result")
            return cached_result

        logger.info("Processing transcript for analysis...")

        # 1. Extract decisions
        logger.info("Extracting decisions...")
        decisions = extract_decisions(request.transcript_text)

        # 2. Extract action items
        logger.info("Extracting action items...")
        action_items = extract_action_items(request.transcript_text)

        # 3. Extract dependencies
        logger.info("Extracting dependencies...")
        dependencies = extract_dependencies(
            request.transcript_text,
            decisions,
            action_items,
        )

        # 4. Validate decisions
        logger.info("Validating decisions...")
        decision_validation = validate_decisions(decisions)

        # 5. Validate action items
        logger.info("Validating action items...")
        action_validation = validate_actions(action_items)

        # 6. Detect conflicts
        logger.info("Detecting conflicts...")
        conflicts = detect_conflicts(decisions, action_items, dependencies)

        # Build response
        response = AnalyzeResponse(
            decisions=decisions,
            action_items=action_items,
            dependencies=dependencies,
            validation={
                "decisions": decision_validation,
                "actions": action_validation,
            },
            conflicts=conflicts,
            stats={
                "decision_count": len(decisions),
                "action_count": len(action_items),
                "dependency_count": len(dependencies),
                "owner_count": len(
                    set(a.owner for a in action_items if a.owner)
                ),
                "high_priority_count": sum(
                    1 for a in action_items if a.priority == "high"
                ),
            },
        )

        logger.info(
            f"Analysis complete: {len(decisions)} decisions, "
            f"{len(action_items)} actions, {len(dependencies)} dependencies"
        )

        # Cache the result
        analysis_cache.set(request.transcript_text, response)
        logger.info(f"Cached analysis result. Cache size: {analysis_cache.size()}")

        return response

    except HTTPException:
        raise
    except ResourceExhausted as e:
        logger.error(f"Gemini quota exceeded: {e}")
        raise HTTPException(
            status_code=429,
            detail="Gemini API quota exceeded. Please retry later or use an API key with billing enabled.",
        )
    except Exception as e:
        logger.error(f"Error analyzing transcript: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing transcript: {str(e)}",
        )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Patchamomma API",
        "version": "1.0.0",
        "docs": "/docs",
    }
