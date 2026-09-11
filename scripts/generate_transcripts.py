"""Generate realistic meeting transcripts for testing."""

import json
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Realistic meeting transcripts
MEETINGS = [
    {
        "meeting_id": "SPRINT_PLANNING_001",
        "title": "Sprint Planning - Q4 Initiative",
        "duration_minutes": 45,
        "speakers": [
            {"id": "PM", "name": "Sarah Chen (Product Manager)"},
            {"id": "ENG", "name": "Marcus Johnson (Engineering Lead)"},
            {"id": "DESIGN", "name": "Lisa Wong (Design Lead)"},
            {"id": "QA", "name": "David Kumar (QA Manager)"},
        ],
        "segments": [
            {
                "timestamp": "00:00:30",
                "speaker": "PM",
                "speaker_name": "Sarah Chen",
                "text": "Welcome everyone to our sprint planning meeting. We have a lot to cover today, so let's get started. First, we need to decide on our tech stack for the new dashboard project."
            },
            {
                "timestamp": "00:02:15",
                "speaker": "ENG",
                "speaker_name": "Marcus Johnson",
                "text": "I've been evaluating several options. I recommend React for the frontend because of its component reusability and strong ecosystem. For the backend, Node.js with Express would be perfect for rapid development."
            },
            {
                "timestamp": "00:04:00",
                "speaker": "DESIGN",
                "speaker_name": "Lisa Wong",
                "text": "React works great for us. I can design reusable component libraries that developers can use directly. Plus, the developer experience with hot reload will speed up our workflow."
            },
            {
                "timestamp": "00:05:45",
                "speaker": "PM",
                "speaker_name": "Sarah Chen",
                "text": "Excellent. So we've decided on React and Node.js. Marcus, when can you have the development environment set up?"
            },
            {
                "timestamp": "00:06:30",
                "speaker": "ENG",
                "speaker_name": "Marcus Johnson",
                "text": "I can have everything ready by next Friday. I'll also write comprehensive setup documentation so everyone can get started immediately."
            },
            {
                "timestamp": "00:08:00",
                "speaker": "QA",
                "speaker_name": "David Kumar",
                "text": "What about testing strategy? Should we implement unit tests, integration tests, or both?"
            },
            {
                "timestamp": "00:09:15",
                "speaker": "PM",
                "speaker_name": "Sarah Chen",
                "text": "Good question. I want us to aim for at least 80% code coverage. We'll need both unit and integration tests. David, can you create a detailed testing plan?"
            },
            {
                "timestamp": "00:10:30",
                "speaker": "QA",
                "speaker_name": "David Kumar",
                "text": "I'll have a comprehensive testing strategy document ready by Wednesday. This will include test categories, coverage goals, and automation framework recommendations."
            },
            {
                "timestamp": "00:12:00",
                "speaker": "DESIGN",
                "speaker_name": "Lisa Wong",
                "text": "When do you need the UI mockups? I want to make sure the design is validated before engineering starts implementation."
            },
            {
                "timestamp": "00:13:00",
                "speaker": "PM",
                "speaker_name": "Sarah Chen",
                "text": "Please have the mockups ready by next Tuesday. This way, Marcus's team can review and start implementation by Wednesday."
            },
            {
                "timestamp": "00:14:30",
                "speaker": "ENG",
                "speaker_name": "Marcus Johnson",
                "text": "We should also set up CI/CD pipelines. I'm thinking GitHub Actions for automated testing and deployment to staging."
            },
            {
                "timestamp": "00:16:00",
                "speaker": "PM",
                "speaker_name": "Sarah Chen",
                "text": "Perfect. Marcus, set up the CI/CD pipeline by the end of next week. And let's schedule a design review meeting for Thursday to discuss the mockups."
            },
            {
                "timestamp": "00:17:30",
                "speaker": "QA",
                "speaker_name": "David Kumar",
                "text": "Should we also plan for performance testing? The dashboard needs to handle large datasets efficiently."
            },
            {
                "timestamp": "00:18:45",
                "speaker": "PM",
                "speaker_name": "Sarah Chen",
                "text": "Yes, performance is critical. We should test with datasets of at least 100k records. David, include this in your testing plan."
            },
            {
                "timestamp": "00:20:00",
                "speaker": "ENG",
                "speaker_name": "Marcus Johnson",
                "text": "I'll implement database indexing and query optimization to ensure good performance. We might also need to implement pagination or lazy loading."
            },
        ],
    },
    {
        "meeting_id": "ARCHITECTURE_REVIEW_002",
        "title": "Architecture Review - Microservices Migration",
        "duration_minutes": 60,
        "speakers": [
            {"id": "ARCH", "name": "James Wilson (Solutions Architect)"},
            {"id": "BACKEND", "name": "Priya Patel (Backend Lead)"},
            {"id": "OPS", "name": "Alex Chen (DevOps Engineer)"},
            {"id": "SECURITY", "name": "Emma Thompson (Security Officer)"},
        ],
        "segments": [
            {
                "timestamp": "00:00:45",
                "speaker": "ARCH",
                "speaker_name": "James Wilson",
                "text": "Thank you all for joining. Today we're discussing the migration from our monolithic architecture to microservices. This is a critical decision that will impact our scalability and development velocity."
            },
            {
                "timestamp": "00:02:30",
                "speaker": "BACKEND",
                "speaker_name": "Priya Patel",
                "text": "I've analyzed our codebase. I recommend breaking it into 5 microservices: User Service, Product Service, Order Service, Payment Service, and Notification Service. Each can be developed and deployed independently."
            },
            {
                "timestamp": "00:05:00",
                "speaker": "OPS",
                "speaker_name": "Alex Chen",
                "text": "Microservices will require changes to our deployment infrastructure. We'll need Kubernetes for orchestration and proper monitoring. I estimate 3 weeks to set up the infrastructure."
            },
            {
                "timestamp": "00:07:15",
                "speaker": "SECURITY",
                "speaker_name": "Emma Thompson",
                "text": "Security is a major concern with microservices. We need to implement service-to-service authentication, API gateways, and proper network segmentation."
            },
            {
                "timestamp": "00:09:00",
                "speaker": "ARCH",
                "speaker_name": "James Wilson",
                "text": "Good points. Let's decide on using Kong as our API Gateway and implement mutual TLS for service-to-service communication. Priya, can you lead the architecture documentation?"
            },
            {
                "timestamp": "00:10:30",
                "speaker": "BACKEND",
                "speaker_name": "Priya Patel",
                "text": "I'll create detailed architecture diagrams and service specifications. I can have the first draft ready in two weeks."
            },
            {
                "timestamp": "00:12:00",
                "speaker": "OPS",
                "speaker_name": "Alex Chen",
                "text": "We should also plan the data migration strategy. Some services will need their own databases. This is complex and needs careful planning."
            },
            {
                "timestamp": "00:14:15",
                "speaker": "SECURITY",
                "speaker_name": "Emma Thompson",
                "text": "I'll create a security assessment document. We need to ensure PCI compliance for the Payment Service and proper encryption everywhere."
            },
            {
                "timestamp": "00:16:00",
                "speaker": "ARCH",
                "speaker_name": "James Wilson",
                "text": "Timeline: Start with infrastructure setup (3 weeks), parallel with architecture documentation (2 weeks). Full migration target is 3 months. Does everyone agree?"
            },
            {
                "timestamp": "00:18:00",
                "speaker": "BACKEND",
                "speaker_name": "Priya Patel",
                "text": "Agreed, but we need to ensure backward compatibility during the migration. I propose a phased rollout starting with the Notification Service."
            },
            {
                "timestamp": "00:20:00",
                "speaker": "OPS",
                "speaker_name": "Alex Chen",
                "text": "I'll set up staging Kubernetes cluster by next month. We should start load testing immediately after infrastructure is ready."
            },
        ],
    },
    {
        "meeting_id": "SECURITY_AUDIT_003",
        "title": "Security Audit & Compliance Review",
        "duration_minutes": 40,
        "speakers": [
            {"id": "CSEC", "name": "Robert Kim (Chief Security Officer)"},
            {"id": "AUDIT", "name": "Jennifer Martinez (Compliance Officer)"},
            {"id": "DEV", "name": "Thomas Brown (Senior Developer)"},
        ],
        "segments": [
            {
                "timestamp": "00:01:00",
                "speaker": "CSEC",
                "speaker_name": "Robert Kim",
                "text": "Our security audit found several critical issues. First, we have hardcoded credentials in our codebase. This must be fixed immediately."
            },
            {
                "timestamp": "00:02:30",
                "speaker": "DEV",
                "speaker_name": "Thomas Brown",
                "text": "I'll audit the entire codebase and remove all hardcoded secrets. We'll use environment variables and AWS Secrets Manager for credential management."
            },
            {
                "timestamp": "00:04:00",
                "speaker": "AUDIT",
                "speaker_name": "Jennifer Martinez",
                "text": "We also need to comply with GDPR and CCPA. All user data must be encrypted and we need clear data retention policies."
            },
            {
                "timestamp": "00:05:45",
                "speaker": "CSEC",
                "speaker_name": "Robert Kim",
                "text": "Thomas, implement AES-256 encryption for all sensitive data at rest. For data in transit, enforce TLS 1.3."
            },
            {
                "timestamp": "00:07:15",
                "speaker": "DEV",
                "speaker_name": "Thomas Brown",
                "text": "I'll implement encryption this week. I also recommend we run OWASP security tests and fix any vulnerabilities found."
            },
            {
                "timestamp": "00:09:00",
                "speaker": "AUDIT",
                "speaker_name": "Jennifer Martinez",
                "text": "We need a comprehensive data classification and retention policy. Can you draft this by next Friday?"
            },
            {
                "timestamp": "00:10:30",
                "speaker": "CSEC",
                "speaker_name": "Robert Kim",
                "text": "Also, implement multi-factor authentication for all admin accounts. This is non-negotiable."
            },
            {
                "timestamp": "00:12:00",
                "speaker": "DEV",
                "speaker_name": "Thomas Brown",
                "text": "MFA will be ready by end of week. I'm also setting up automated security scanning in our CI/CD pipeline."
            },
            {
                "timestamp": "00:14:00",
                "speaker": "AUDIT",
                "speaker_name": "Jennifer Martinez",
                "text": "We should schedule a follow-up audit in 30 days. All critical issues must be resolved by then."
            },
            {
                "timestamp": "00:15:30",
                "speaker": "CSEC",
                "speaker_name": "Robert Kim",
                "text": "Agreed. Thomas, send weekly progress reports. Jennifer, prepare the compliance checklist."
            },
        ],
    },
    {
        "meeting_id": "PRODUCT_ROADMAP_004",
        "title": "Product Roadmap Planning - H2 2024",
        "duration_minutes": 55,
        "speakers": [
            {"id": "SVP", "name": "Victoria Lane (SVP Product)"},
            {"id": "PM1", "name": "Alex Martinez (Product Manager)"},
            {"id": "PM2", "name": "Nina Singh (Senior Product Manager)"},
            {"id": "MKTG", "name": "Kevin Park (Marketing Manager)"},
        ],
        "segments": [
            {
                "timestamp": "00:01:00",
                "speaker": "SVP",
                "speaker_name": "Victoria Lane",
                "text": "Let's discuss our H2 roadmap. We need to align on priorities. Market research shows customers want better mobile experience and AI-powered features."
            },
            {
                "timestamp": "00:03:00",
                "speaker": "PM1",
                "speaker_name": "Alex Martinez",
                "text": "I propose three major initiatives: Mobile app redesign, AI-powered recommendations, and advanced analytics dashboard."
            },
            {
                "timestamp": "00:05:15",
                "speaker": "PM2",
                "speaker_name": "Nina Singh",
                "text": "I agree with the priorities. For mobile, we should focus on iOS first since that's 60% of our user base. Android can follow in Q4."
            },
            {
                "timestamp": "00:07:00",
                "speaker": "MKTG",
                "speaker_name": "Kevin Park",
                "text": "From marketing perspective, the AI features are most exciting for positioning. We can build a strong narrative around intelligent recommendations."
            },
            {
                "timestamp": "00:08:30",
                "speaker": "SVP",
                "speaker_name": "Victoria Lane",
                "text": "Timeline: iOS launch by September 30th, AI recommendations by October 31st, Advanced analytics by November 30th. Is this realistic?"
            },
            {
                "timestamp": "00:10:00",
                "speaker": "PM1",
                "speaker_name": "Alex Martinez",
                "text": "iOS is achievable. But AI recommendations require data science work. We need to hire or allocate resources immediately."
            },
            {
                "timestamp": "00:12:00",
                "speaker": "PM2",
                "speaker_name": "Nina Singh",
                "text": "I recommend we start with basic collaborative filtering and upgrade to ML models in Q1. This keeps us on schedule."
            },
            {
                "timestamp": "00:13:45",
                "speaker": "MKTG",
                "speaker_name": "Kevin Park",
                "text": "For marketing, we need at least 2 weeks before launch for campaign preparation. Please provide feature list and screenshots by September 1st."
            },
            {
                "timestamp": "00:15:30",
                "speaker": "SVP",
                "speaker_name": "Victoria Lane",
                "text": "Alex, prepare detailed requirements for iOS app by next Friday. Nina, draft the AI feature specification. Kevin, create marketing brief."
            },
            {
                "timestamp": "00:17:00",
                "speaker": "PM1",
                "speaker_name": "Alex Martinez",
                "text": "I'll also coordinate with engineering to understand technical feasibility and resource requirements."
            },
            {
                "timestamp": "00:18:30",
                "speaker": "SVP",
                "speaker_name": "Victoria Lane",
                "text": "Let's meet again next Wednesday to review drafts and confirm timelines. This roadmap will be our north star for H2."
            },
        ],
    },
    {
        "meeting_id": "QUARTERLY_RETRO_005",
        "title": "Q3 Retrospective & Lessons Learned",
        "duration_minutes": 50,
        "speakers": [
            {"id": "LEAD", "name": "Michael Scott (Team Lead)"},
            {"id": "MEM1", "name": "Rachel Green (Developer)"},
            {"id": "MEM2", "name": "Chandler Bing (Developer)"},
            {"id": "MEM3", "name": "Monica Geller (QA Engineer)"},
        ],
        "segments": [
            {
                "timestamp": "00:01:30",
                "speaker": "LEAD",
                "speaker_name": "Michael Scott",
                "text": "Great Q3, team! We shipped 8 major features and hit 95% of our sprint commitments. Let's discuss what went well and what we can improve."
            },
            {
                "timestamp": "00:03:00",
                "speaker": "MEM1",
                "speaker_name": "Rachel Green",
                "text": "I think our standups were really effective. Having clear daily goals helped us identify blockers early. We should keep this practice."
            },
            {
                "timestamp": "00:04:30",
                "speaker": "MEM2",
                "speaker_name": "Chandler Bing",
                "text": "Agreed. But I noticed our code review process was sometimes slow. We should establish SLA for code reviews - maybe 24 hours maximum."
            },
            {
                "timestamp": "00:06:00",
                "speaker": "MEM3",
                "speaker_name": "Monica Geller",
                "text": "Quality improved significantly. We had fewer production bugs this quarter. The testing improvements we made really helped."
            },
            {
                "timestamp": "00:07:45",
                "speaker": "LEAD",
                "speaker_name": "Michael Scott",
                "text": "Excellent observation. Monica, let's document what worked in testing and make it standard practice. What were the key improvements?"
            },
            {
                "timestamp": "00:09:15",
                "speaker": "MEM3",
                "speaker_name": "Monica Geller",
                "text": "We implemented automated integration tests and started testing on actual devices. This caught real issues that unit tests missed."
            },
            {
                "timestamp": "00:11:00",
                "speaker": "MEM1",
                "speaker_name": "Rachel Green",
                "text": "One challenge was the last-minute feature requests. They disrupted our sprint planning. Can we be more strict about scope?"
            },
            {
                "timestamp": "00:12:30",
                "speaker": "LEAD",
                "speaker_name": "Michael Scott",
                "text": "Valid point. We'll implement a hard freeze 48 hours before sprint end. Anything else needs to wait for next sprint."
            },
            {
                "timestamp": "00:14:00",
                "speaker": "MEM2",
                "speaker_name": "Chandler Bing",
                "text": "I also want to suggest we do more knowledge sharing. Some team members had expertise that wasn't being leveraged."
            },
            {
                "timestamp": "00:15:30",
                "speaker": "LEAD",
                "speaker_name": "Michael Scott",
                "text": "Great idea. Let's schedule weekly tech talks. Each team member presents something they learned. Who wants to go first in Q4?"
            },
            {
                "timestamp": "00:17:00",
                "speaker": "MEM1",
                "speaker_name": "Rachel Green",
                "text": "I'll present on the new API design patterns we used this quarter."
            },
            {
                "timestamp": "00:18:30",
                "speaker": "LEAD",
                "speaker_name": "Michael Scott",
                "text": "Perfect. Let's also implement a 24-hour code review SLA and document our testing best practices. I'll schedule the first tech talk for next week."
            },
        ],
    },
]


def generate_transcripts():
    """Generate realistic meeting transcripts."""
    output_dir = Path("tests/fixtures/sample_transcripts")
    output_dir.mkdir(parents=True, exist_ok=True)

    for meeting in MEETINGS:
        # Convert to JSON format
        transcript = {
            "meeting_id": meeting["meeting_id"],
            "title": meeting["title"],
            "duration_minutes": meeting["duration_minutes"],
            "speakers": meeting["speakers"],
            "segments": meeting["segments"],
            "generated_at": datetime.now().isoformat(),
        }

        # Save to file
        output_file = output_dir / f"{meeting['meeting_id']}.json"
        with open(output_file, "w") as f:
            json.dump(transcript, f, indent=2)

        logger.info(f"✅ Generated {output_file}")
        logger.info(
            f"   📊 {len(meeting['segments'])} segments, "
            f"{len(meeting['speakers'])} speakers, "
            f"{meeting['duration_minutes']} minutes"
        )

    logger.info(f"\n✅ Generated {len(MEETINGS)} realistic meeting transcripts!")
    logger.info(f"📁 Location: {output_dir}")
    logger.info("\n📋 Meetings Generated:")
    for meeting in MEETINGS:
        logger.info(f"  - {meeting['title']} ({meeting['meeting_id']})")


if __name__ == "__main__":
    generate_transcripts()
