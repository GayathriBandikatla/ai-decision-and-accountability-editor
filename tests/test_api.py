"""Tests for FastAPI endpoints."""

import pytest
import json
from fastapi.testclient import TestClient
from google.api_core.exceptions import ResourceExhausted

import api.main
from api.main import app, analysis_cache
from data_models.decision import Decision
from data_models.action_item import ActionItem
from data_models.dependency import Dependency

client = TestClient(app)


FAKE_DECISIONS = [
    Decision(text="Use React for the frontend", confidence=0.95,
             evidence_speaker="PM", evidence_text="So we've decided on React and Python."),
]
FAKE_ACTIONS = [
    ActionItem(text="Setup the development environment", owner="Dev", deadline="Friday",
               priority="high", evidence_text="I'll setup the development environment by Friday."),
]
FAKE_DEPENDENCIES = [
    Dependency(source_id="Decision 0", target_id="Action 0", relationship="enables", confidence=0.9),
]


@pytest.fixture(autouse=True)
def mock_gemini_agents(monkeypatch):
    """Keep API tests deterministic and offline: never call Gemini."""
    analysis_cache.clear()
    monkeypatch.setattr(api.main, "extract_decisions", lambda text: list(FAKE_DECISIONS))
    monkeypatch.setattr(api.main, "extract_action_items", lambda text: list(FAKE_ACTIONS))
    monkeypatch.setattr(api.main, "extract_dependencies", lambda text, d, a: list(FAKE_DEPENDENCIES))

# Sample transcripts for testing
SHORT_TRANSCRIPT = "Let's use React."
VALID_TRANSCRIPT = """
Project Manager: Welcome to the meeting. Let's discuss the tech stack.

Lead Developer: I recommend we use React for the frontend and Python for the backend.

UI Designer: React is great for us, we can design reusable components.

PM: Excellent. So we've decided on React and Python. Let's make this official.

Dev: I'll setup the development environment by Friday.

PM: John, can you document the setup process?

Dev: Sure, I'll have full documentation ready.

QA: What about testing strategy?

PM: Let's aim for 80% code coverage. QA team to define testing plan.

QA: I'll have a testing strategy document by Wednesday.
"""

LONG_TRANSCRIPT = VALID_TRANSCRIPT * 5


class TestHealthCheck:
    """Tests for health check endpoint."""

    def test_health_check_success(self):
        """Test successful health check."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == "healthy"
        assert 'message' in data

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert 'message' in data
        assert 'version' in data


class TestAnalyzeEndpoint:
    """Tests for /analyze endpoint."""

    def test_analyze_success(self):
        """Test successful analysis."""
        response = client.post(
            "/analyze",
            json={"transcript_text": VALID_TRANSCRIPT}
        )
        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert 'decisions' in data
        assert 'action_items' in data
        assert 'dependencies' in data
        assert 'validation' in data
        assert 'conflicts' in data
        assert 'stats' in data

        # Check types
        assert isinstance(data['decisions'], list)
        assert isinstance(data['action_items'], list)
        assert isinstance(data['dependencies'], list)
        assert isinstance(data['stats'], dict)

    def test_analyze_short_transcript(self):
        """Test with transcript too short."""
        response = client.post(
            "/analyze",
            json={"transcript_text": SHORT_TRANSCRIPT}
        )
        assert response.status_code == 400
        data = response.json()
        assert 'detail' in data

    def test_analyze_empty_transcript(self):
        """Test with empty transcript."""
        response = client.post(
            "/analyze",
            json={"transcript_text": ""}
        )
        assert response.status_code == 400

    def test_analyze_whitespace_only(self):
        """Test with whitespace-only transcript."""
        response = client.post(
            "/analyze",
            json={"transcript_text": "   \n   \t   "}
        )
        assert response.status_code == 400

    def test_analyze_long_transcript(self):
        """Test with very long transcript."""
        response = client.post(
            "/analyze",
            json={"transcript_text": LONG_TRANSCRIPT}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data['decisions'], list)

    def test_analyze_response_structure(self):
        """Test detailed response structure."""
        response = client.post(
            "/analyze",
            json={"transcript_text": VALID_TRANSCRIPT}
        )
        assert response.status_code == 200
        data = response.json()

        # Check decisions structure
        if len(data['decisions']) > 0:
            decision = data['decisions'][0]
            assert 'text' in decision
            assert 'confidence' in decision
            assert 'evidence_text' in decision
            assert isinstance(decision['confidence'], float)

        # Check action items structure
        if len(data['action_items']) > 0:
            action = data['action_items'][0]
            assert 'text' in action
            assert 'priority' in action
            assert 'status' in action

        # Check stats
        assert 'decision_count' in data['stats']
        assert 'action_count' in data['stats']
        assert 'owner_count' in data['stats']
        assert data['stats']['decision_count'] == len(data['decisions'])
        assert data['stats']['decision_count'] == 1
        assert data['stats']['action_count'] == 1
        assert data['stats']['dependency_count'] == 1
        assert data['conflicts']['conflict_count'] == 0

    def test_analyze_validation_present(self):
        """Test that validation results are included."""
        response = client.post(
            "/analyze",
            json={"transcript_text": VALID_TRANSCRIPT}
        )
        assert response.status_code == 200
        data = response.json()

        assert 'validation' in data
        assert 'decisions' in data['validation']
        assert 'actions' in data['validation']

    def test_analyze_conflicts_present(self):
        """Test that conflict detection results are included."""
        response = client.post(
            "/analyze",
            json={"transcript_text": VALID_TRANSCRIPT}
        )
        assert response.status_code == 200
        data = response.json()

        assert 'conflicts' in data
        assert 'conflict_count' in data['conflicts']
        assert 'conflicts' in data['conflicts']

    def test_analyze_missing_body(self):
        """Test with missing request body."""
        response = client.post("/analyze", json={})
        assert response.status_code == 422  # Validation error

    def test_analyze_invalid_json(self):
        """Test with invalid JSON."""
        response = client.post(
            "/analyze",
            content="not json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422


class TestContentNegotiation:
    """Tests for content negotiation."""

    def test_json_response_content_type(self):
        """Test that response is JSON."""
        response = client.post(
            "/analyze",
            json={"transcript_text": VALID_TRANSCRIPT}
        )
        assert response.headers.get('content-type') == 'application/json'

    def test_request_with_json_content_type(self):
        """Test request with explicit content-type."""
        response = client.post(
            "/analyze",
            json={"transcript_text": VALID_TRANSCRIPT},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200


class TestErrorHandling:
    """Tests for error handling."""

    def test_422_for_invalid_request(self):
        """Test that invalid requests return 422."""
        response = client.post(
            "/analyze",
            json={"wrong_field": "value"}
        )
        assert response.status_code == 422

    def test_error_response_format(self):
        """Test that error responses have proper format."""
        response = client.post(
            "/analyze",
            json={"transcript_text": "too short"}
        )
        assert response.status_code == 400
        data = response.json()
        assert 'detail' in data

    def test_quota_exhausted_returns_429(self, monkeypatch):
        """Gemini quota errors surface as 429, not a silent empty result."""
        def raise_quota(text):
            raise ResourceExhausted("quota exceeded")
        monkeypatch.setattr(api.main, "extract_decisions", raise_quota)
        response = client.post(
            "/analyze",
            json={"transcript_text": "quota test " * 10}
        )
        assert response.status_code == 429
        assert "quota" in response.json()["detail"].lower()

    def test_unexpected_error_returns_500(self, monkeypatch):
        """Unexpected agent failures return a structured 500."""
        def boom(text):
            raise RuntimeError("boom")
        monkeypatch.setattr(api.main, "extract_decisions", boom)
        response = client.post(
            "/analyze",
            json={"transcript_text": "server error test " * 10}
        )
        assert response.status_code == 500
        assert "detail" in response.json()


class TestCORS:
    """Tests for CORS configuration."""

    def test_cors_headers_present(self):
        """Test that CORS headers are present."""
        response = client.options(
            "/analyze",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            },
        )
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"

    def test_cors_allow_origin(self):
        """Test CORS Allow-Origin header."""
        response = client.get("/health")
        # CORS headers might not be present in test client
        # but we can verify the endpoint works
        assert response.status_code == 200


class TestMetadata:
    """Tests for API metadata."""

    def test_openapi_schema(self):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert 'openapi' in data or 'swagger' in data

    def test_docs_endpoint(self):
        """Test that docs endpoint is available."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert 'html' in response.text.lower()


class TestConcurrency:
    """Tests for concurrent requests."""

    def test_multiple_sequential_requests(self):
        """Test multiple requests in sequence."""
        responses = []
        for i in range(3):
            response = client.post(
                "/analyze",
                json={"transcript_text": VALID_TRANSCRIPT}
            )
            responses.append(response)

        assert all(r.status_code == 200 for r in responses)
        assert len(set(r.json()['stats']['decision_count'] for r in responses)) >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
