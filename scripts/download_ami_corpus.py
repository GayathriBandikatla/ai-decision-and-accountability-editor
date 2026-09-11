"""Download and parse AMI Corpus meeting transcripts."""

import json
import logging
from pathlib import Path
from datetime import datetime
import requests
from xml.etree import ElementTree as ET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample meetings from AMI Corpus
# You can add more from: https://groups.inf.ed.ac.uk/ami/corpus/
SAMPLE_MEETINGS = [
    "ES2003a",
    "ES2003b",
    "ES2003c",
    "IB4003",
    "IB4004",
]

# Base URL for AMI Corpus (you may need to adjust based on actual server)
AMI_BASE_URL = "https://groups.inf.ed.ac.uk/ami/corpus/amicorpus"


def generate_sample_transcripts() -> None:
    """Generate sample meeting transcripts in JSON format."""

    output_dir = Path("tests/fixtures/sample_transcripts")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Since AMI Corpus direct download may require manual access,
    # we'll create realistic sample transcripts for testing
    sample_meetings = [
        {
            "meeting_id": "PRJ001",
            "duration_minutes": 30,
            "speakers": [
                {"id": "PM", "name": "Project Manager"},
                {"id": "DEV", "name": "Lead Developer"},
                {"id": "UI", "name": "UI Designer"},
                {"id": "QA", "name": "QA Engineer"},
            ],
            "segments": [
                {
                    "timestamp": "00:00:15",
                    "speaker": "PM",
                    "speaker_name": "Project Manager",
                    "text": "Welcome everyone. Let's discuss the next phase of the project. We need to finalize our tech stack and timeline.",
                },
                {
                    "timestamp": "00:01:00",
                    "speaker": "DEV",
                    "speaker_name": "Lead Developer",
                    "text": "I propose we use React for the frontend and Python with FastAPI for the backend. It aligns with our team's expertise.",
                },
                {
                    "timestamp": "00:02:30",
                    "speaker": "UI",
                    "speaker_name": "UI Designer",
                    "text": "React works great for us. We can design components reusably.",
                },
                {
                    "timestamp": "00:03:45",
                    "speaker": "PM",
                    "speaker_name": "Project Manager",
                    "text": "Great, so we've decided on React and Python. Development starts next week. Dev, can you setup the development environment?",
                },
                {
                    "timestamp": "00:04:30",
                    "speaker": "DEV",
                    "speaker_name": "Lead Developer",
                    "text": "Sure, I'll have it ready by Friday. I'll also document the setup process.",
                },
                {
                    "timestamp": "00:05:45",
                    "speaker": "QA",
                    "speaker_name": "QA Engineer",
                    "text": "We should define testing strategy early. I recommend automated tests for backend and end-to-end tests for frontend.",
                },
                {
                    "timestamp": "00:07:00",
                    "speaker": "PM",
                    "speaker_name": "Project Manager",
                    "text": "Good point. Let's aim for 80% code coverage. QA, please document the testing plan by next Wednesday.",
                },
                {
                    "timestamp": "00:08:30",
                    "speaker": "DEV",
                    "speaker_name": "Lead Developer",
                    "text": "We'll need to deploy to Cloud Run. I suggest using Docker for containerization.",
                },
                {
                    "timestamp": "00:09:45",
                    "speaker": "PM",
                    "speaker_name": "Project Manager",
                    "text": "Perfect. Let's use Google Cloud infrastructure. Dev, please setup CI/CD pipelines by Sept 1st.",
                },
                {
                    "timestamp": "00:11:00",
                    "speaker": "UI",
                    "speaker_name": "UI Designer",
                    "text": "When do we need the design mockups? I can start creating them this week.",
                },
                {
                    "timestamp": "00:12:15",
                    "speaker": "PM",
                    "speaker_name": "Project Manager",
                    "text": "Please share mockups by next Friday so dev can start implementation.",
                },
                {
                    "timestamp": "00:13:30",
                    "speaker": "QA",
                    "speaker_name": "QA Engineer",
                    "text": "We should also plan for user acceptance testing. Can we schedule a demo in 2 weeks?",
                },
                {
                    "timestamp": "00:15:00",
                    "speaker": "PM",
                    "speaker_name": "Project Manager",
                    "text": "Yes, let's schedule UAT for September 5th. Everyone should be prepared to present their work.",
                },
            ],
        },
        {
            "meeting_id": "PRJ002",
            "duration_minutes": 25,
            "speakers": [
                {"id": "PM", "name": "Project Manager"},
                {"id": "DEV", "name": "Lead Developer"},
                {"id": "OPS", "name": "Operations Manager"},
            ],
            "segments": [
                {
                    "timestamp": "00:00:10",
                    "speaker": "PM",
                    "speaker_name": "Project Manager",
                    "text": "Quick sync on the infrastructure. What's the status, Operations?",
                },
                {
                    "timestamp": "00:00:45",
                    "speaker": "OPS",
                    "speaker_name": "Operations Manager",
                    "text": "We're setting up the Cloud Run environment. Database is PostgreSQL on Cloud SQL.",
                },
                {
                    "timestamp": "00:02:00",
                    "speaker": "DEV",
                    "speaker_name": "Lead Developer",
                    "text": "Good. We'll use BigQuery for analytics and Firestore for real-time features.",
                },
                {
                    "timestamp": "00:03:30",
                    "speaker": "PM",
                    "speaker_name": "Project Manager",
                    "text": "Sounds solid. OPS, please ensure all infrastructure is ready by August 31st.",
                },
                {
                    "timestamp": "00:04:45",
                    "speaker": "OPS",
                    "speaker_name": "Operations Manager",
                    "text": "Will do. I'll also setup monitoring and logging with Cloud Logging.",
                },
                {
                    "timestamp": "00:06:00",
                    "speaker": "DEV",
                    "speaker_name": "Lead Developer",
                    "text": "We need to decide on API rate limiting and caching strategies.",
                },
                {
                    "timestamp": "00:07:15",
                    "speaker": "PM",
                    "speaker_name": "Project Manager",
                    "text": "Let's use Redis for caching. Dev, please implement rate limiting with Gemini API limits in mind.",
                },
            ],
        },
        {
            "meeting_id": "PRJ003",
            "duration_minutes": 20,
            "speakers": [
                {"id": "TL", "name": "Tech Lead"},
                {"id": "DEV1", "name": "Frontend Dev"},
                {"id": "DEV2", "name": "Backend Dev"},
            ],
            "segments": [
                {
                    "timestamp": "00:00:20",
                    "speaker": "TL",
                    "speaker_name": "Tech Lead",
                    "text": "Let's discuss the API design. Here's the plan: REST endpoints with JSON payloads.",
                },
                {
                    "timestamp": "00:01:30",
                    "speaker": "DEV1",
                    "speaker_name": "Frontend Dev",
                    "text": "Makes sense. I'll implement the client to consume these endpoints using React.",
                },
                {
                    "timestamp": "00:03:00",
                    "speaker": "DEV2",
                    "speaker_name": "Backend Dev",
                    "text": "I'll build the API with FastAPI. We should use Pydantic for validation.",
                },
                {
                    "timestamp": "00:04:30",
                    "speaker": "TL",
                    "speaker_name": "Tech Lead",
                    "text": "Perfect. Frontend and Backend should be in separate repos. Frontend deployed to Cloud Run.",
                },
                {
                    "timestamp": "00:06:00",
                    "speaker": "DEV1",
                    "speaker_name": "Frontend Dev",
                    "text": "Should I use TypeScript or JavaScript? I prefer TypeScript for type safety.",
                },
                {
                    "timestamp": "00:07:15",
                    "speaker": "TL",
                    "speaker_name": "Tech Lead",
                    "text": "Go with TypeScript. It's stricter and prevents runtime errors. Start with the upload component this week.",
                },
                {
                    "timestamp": "00:08:45",
                    "speaker": "DEV2",
                    "speaker_name": "Backend Dev",
                    "text": "I'll have the /analyze endpoint ready by tomorrow. We'll iterate based on frontend needs.",
                },
            ],
        },
        {
            "meeting_id": "PRJ004",
            "duration_minutes": 22,
            "speakers": [
                {"id": "PM", "name": "Product Manager"},
                {"id": "DEV", "name": "Senior Developer"},
                {"id": "SEC", "name": "Security Officer"},
            ],
            "segments": [
                {
                    "timestamp": "00:00:30",
                    "speaker": "PM",
                    "speaker_name": "Product Manager",
                    "text": "Security is critical. Let's discuss threat model and compliance requirements.",
                },
                {
                    "timestamp": "00:02:00",
                    "speaker": "SEC",
                    "speaker_name": "Security Officer",
                    "text": "We need to encrypt all sensitive data at rest and in transit. API keys must never be hardcoded.",
                },
                {
                    "timestamp": "00:03:30",
                    "speaker": "DEV",
                    "speaker_name": "Senior Developer",
                    "text": "Agreed. We'll use environment variables for secrets. I'll implement TLS for all endpoints.",
                },
                {
                    "timestamp": "00:05:00",
                    "speaker": "SEC",
                    "speaker_name": "Security Officer",
                    "text": "Good. Also, all user inputs must be validated. No SQL injection or XSS vulnerabilities.",
                },
                {
                    "timestamp": "00:06:30",
                    "speaker": "PM",
                    "speaker_name": "Product Manager",
                    "text": "Dev, please implement input validation using Pydantic. When can you have security testing done?",
                },
                {
                    "timestamp": "00:08:00",
                    "speaker": "DEV",
                    "speaker_name": "Senior Developer",
                    "text": "I'll run OWASP Top 10 checks by September 1st. I'll also setup Secret Manager for credentials.",
                },
                {
                    "timestamp": "00:09:30",
                    "speaker": "SEC",
                    "speaker_name": "Security Officer",
                    "text": "Excellent. Let's also implement rate limiting to prevent abuse.",
                },
                {
                    "timestamp": "00:11:00",
                    "speaker": "PM",
                    "speaker_name": "Product Manager",
                    "text": "Rate limiting is critical. Dev, implement this by next week. Security clearance needed before launch.",
                },
            ],
        },
        {
            "meeting_id": "PRJ005",
            "duration_minutes": 28,
            "speakers": [
                {"id": "PM", "name": "Project Manager"},
                {"id": "AR", "name": "Architect"},
                {"id": "QA", "name": "QA Lead"},
            ],
            "segments": [
                {
                    "timestamp": "00:00:45",
                    "speaker": "PM",
                    "speaker_name": "Project Manager",
                    "text": "Final checkpoint coming up. Let's ensure we're on track. Architecture review, please.",
                },
                {
                    "timestamp": "00:02:15",
                    "speaker": "AR",
                    "speaker_name": "Architect",
                    "text": "System is modular and loosely coupled. We have agents, validators, API, and frontend layers.",
                },
                {
                    "timestamp": "00:03:45",
                    "speaker": "QA",
                    "speaker_name": "QA Lead",
                    "text": "Testing looks good. We have unit tests for validators and integration tests for API.",
                },
                {
                    "timestamp": "00:05:30",
                    "speaker": "PM",
                    "speaker_name": "Project Manager",
                    "text": "Excellent. When can we deploy to Cloud Run?",
                },
                {
                    "timestamp": "00:06:45",
                    "speaker": "AR",
                    "speaker_name": "Architect",
                    "text": "Dockerfile is ready. We can deploy by September 2nd. I'll handle the Cloud Run setup.",
                },
                {
                    "timestamp": "00:08:15",
                    "speaker": "QA",
                    "speaker_name": "QA Lead",
                    "text": "We should do load testing before going live. I'll simulate 100 concurrent users.",
                },
                {
                    "timestamp": "00:09:45",
                    "speaker": "PM",
                    "speaker_name": "Project Manager",
                    "text": "Load testing is important. QA, complete testing by September 3rd. We'll be ready for final submission.",
                },
                {
                    "timestamp": "00:11:30",
                    "speaker": "AR",
                    "speaker_name": "Architect",
                    "text": "I'll also prepare the demo script with all 5 sample transcripts.",
                },
                {
                    "timestamp": "00:13:00",
                    "speaker": "PM",
                    "speaker_name": "Project Manager",
                    "text": "Perfect. By September 5th, we should have a complete, tested, and deployable system.",
                },
            ],
        },
    ]

    # Write sample transcripts to JSON files
    for i, meeting in enumerate(sample_meetings):
        output_file = output_dir / f"{meeting['meeting_id']}.json"
        with open(output_file, "w") as f:
            json.dump(meeting, f, indent=2)
        logger.info(f"✅ Generated {output_file}")

    logger.info(f"\n✅ Generated {len(sample_meetings)} sample transcripts")
    logger.info(
        f"📁 Transcripts saved to: {output_dir}"
    )
    logger.info(
        "\n📖 How to get real AMI Corpus transcripts:"
    )
    logger.info("   1. Visit: https://groups.inf.ed.ac.uk/ami/corpus/")
    logger.info("   2. Download meeting XML files")
    logger.info("   3. Parse them using the parse_ami_xml script")
    logger.info(
        "   4. Or use these sample transcripts for testing"
    )


if __name__ == "__main__":
    generate_sample_transcripts()
