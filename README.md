# Patchamomma: AI Decision & Accountability Auditor

An Agentic AI platform that extracts decisions, action items, owners, deadlines, and dependencies from meeting transcripts using Gemini 2.0 Flash.

## 🎯 Features

- **Decision Extraction**: Automatically identify all decisions made in meetings
- **Action Items**: Extract tasks, assignments, and deadlines with ownership
- **Dependency Mapping**: Identify relationships between decisions and actions
- **Deterministic Validation**: Detect duplicates, missing owners, unrealistic deadlines, and conflicts
- **Evidence Traceability**: Link each decision/action back to the transcript
- **REST API**: FastAPI backend for easy integration
- **Cloud-Ready**: Designed for Google Cloud (BigQuery, Firestore, Cloud Run)

## 🏗️ Architecture

```
Meeting Transcripts (AMI Corpus)
       ↓
[Transcript Loader]
       ↓
┌─────────────────────────────────────┐
│   Gemini 2.0 Flash Agents           │
├─────────────────────────────────────┤
│ • Decision Extractor                │
│ • Action Item Extractor             │
│ • Dependency Mapper                 │
│ + Deterministic Validators          │
└─────────────────────────────────────┘
       ↓
    FastAPI
    ↓
  Results (Decisions, Actions, Validation)
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Secrets

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_key_here
```

**Get your Gemini API key:**
1. Visit https://aistudio.google.com
2. Click "Get API Key"
3. Create a new API key
4. Copy to `.env`

### 3. Generate Sample Data

```bash
# Create realistic sample meeting transcripts
python scripts/download_ami_corpus.py

# This creates 5 sample meetings in tests/fixtures/sample_transcripts/
```

### 4. Run the Backend

```bash
# Start the FastAPI server
python main.py

# API is now running at http://localhost:8000
# Swagger docs: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### 5. Test the API

```bash
# In another terminal, test a simple analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "transcript_text": "Project Manager: Lets use React for frontend. Developer: Agreed. PM: John, setup dev environment by Friday."
  }'
```

## 🐳 Docker for Local Development

### Using Docker Compose

```bash
# Start backend in container
docker-compose up

# Backend runs at http://localhost:8000
# Check health: curl http://localhost:8000/health
```

### Stop

```bash
docker-compose down
```

## 📊 API Endpoints

### POST /analyze

Analyze a meeting transcript and extract all information.

**Request:**
```json
{
  "transcript_text": "Full meeting transcript here..."
}
```

**Response includes:**
- `decisions`: Extracted decisions with evidence
- `action_items`: Tasks with owners and deadlines
- `dependencies`: Relationships between items
- `validation`: Issues found (duplicates, missing data, etc.)
- `conflicts`: Contradictions and problems
- `stats`: Summary numbers

**Example Response:**
```json
{
  "decisions": [
    {
      "text": "Use React for the frontend",
      "confidence": 0.95,
      "evidence_timestamp": "00:05:30",
      "evidence_speaker": "Tech Lead",
      "evidence_text": "...",
      "extracted_at": "2024-08-26T10:00:00"
    }
  ],
  "action_items": [
    {
      "text": "Setup React development environment",
      "owner": "Frontend Developer",
      "deadline": "2024-08-31",
      "priority": "high",
      "status": "open",
      "evidence_text": "..."
    }
  ],
  "dependencies": [...],
  "validation": { ... },
  "conflicts": { ... },
  "stats": {
    "decision_count": 5,
    "action_count": 3,
    "dependency_count": 2,
    "owner_count": 2
  }
}
```

### GET /health

Health check.

```bash
curl http://localhost:8000/health
```

## 📁 Project Structure

```
patchamomma/
├── config/                          # Settings & configuration
│   ├── settings.py                  # Load env vars (.env)
│   └── logging.py                   # Logging setup
├── data_models/                     # Data types (Pydantic)
│   ├── transcript.py                # Meeting structure
│   ├── decision.py                  # Decision model
│   ├── action_item.py               # Action item model
│   └── dependency.py                # Dependency model
├── agents/                          # Gemini agents
│   ├── decision_extractor.py        # Extract decisions
│   ├── action_extractor.py          # Extract action items
│   └── dependency_mapper.py         # Map dependencies
├── validators/                      # Deterministic validation
│   ├── decision_validator.py        # Validate decisions
│   ├── action_validator.py          # Validate actions
│   └── conflict_detector.py         # Detect conflicts
├── api/                             # FastAPI server
│   ├── main.py                      # FastAPI app & routes
│   └── models.py                    # Request/response models
├── tests/                           # Tests & fixtures
│   └── fixtures/
│       └── sample_transcripts/      # Sample meetings (JSON)
├── scripts/                         # Utility scripts
│   └── download_ami_corpus.py       # Generate sample data
├── .env.example                     # Env template
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Container definition
├── docker-compose.yml               # Local dev environment
├── main.py                          # Entry point
├── DEVELOPMENT_GUIDE.md             # Development reference
└── README.md                        # This file
```

## 🧪 Testing

### Test with Sample Transcripts

```bash
# List available samples
ls tests/fixtures/sample_transcripts/

# Load and analyze one
python -c "
import json
from agents import extract_decisions

with open('tests/fixtures/sample_transcripts/PRJ001.json') as f:
    data = json.load(f)
    
transcript = ' '.join([s['text'] for s in data['segments']])
decisions = extract_decisions(transcript)

for d in decisions:
    print(f'- {d.text} (confidence: {d.confidence:.0%})')
"
```

### Test API Endpoint

```bash
# Start backend in one terminal
python main.py

# In another terminal, test
python -c "
import requests
import json

with open('tests/fixtures/sample_transcripts/PRJ001.json') as f:
    data = json.load(f)
    
transcript = ' '.join([s['text'] for s in data['segments']])

response = requests.post(
    'http://localhost:8000/analyze',
    json={'transcript_text': transcript}
)

result = response.json()
print(f'Decisions: {len(result[\"decisions\"])}')
print(f'Actions: {len(result[\"action_items\"])}')
print(f'Issues: {result[\"validation\"][\"decisions\"][\"issue_count\"]}')
"
```

## 🔐 Security

All sensitive data is managed via environment variables:

- ✅ `GEMINI_API_KEY` - Never committed to git
- ✅ `GCP_CREDENTIALS_PATH` - Service account (optional)
- ✅ `.env` file - Excluded from version control
- ✅ Input validation - Pydantic models validate all requests
- ✅ No secrets in logs - Sensitive data never logged

### .gitignore

```
.env
.env.local
service-account.json
__pycache__/
*.pyc
venv/
node_modules/
.DS_Store
```

## 🎛️ Configuration

### Environment Variables (.env)

```bash
# Gemini API
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.6-flash
GEMINI_FALLBACK_MODELS=gemini-3.5-flash,gemini-3.8-flash,gemini-3.5-flash-lite,gemini-3.1-flash-lite,gemini-flash-lite-latest

# Google Cloud (optional, for future integration)
GCP_PROJECT_ID=your_project_id
GCP_CREDENTIALS_PATH=/path/to/service_account.json

# BigQuery (optional)
BQ_DATASET_ID=patchamomma

# API
API_PORT=8000
API_HOST=0.0.0.0
DEBUG=False
```

## 📝 Example Usage

### Extract Decisions Only

```python
from agents.decision_extractor import extract_decisions

transcript = """
Team Lead: We need to finalize the tech stack.
Developer: I recommend React and Python.
Team Lead: Great, let's go with that.
"""

decisions = extract_decisions(transcript)
for d in decisions:
    print(f"{d.text}")
    print(f"  Confidence: {d.confidence:.0%}")
    print(f"  Evidence: {d.evidence_text}\n")
```

### Extract Action Items

```python
from agents.action_extractor import extract_action_items

action_items = extract_action_items(transcript)
for a in action_items:
    print(f"{a.text}")
    if a.owner:
        print(f"  Owner: {a.owner}")
    if a.deadline:
        print(f"  Deadline: {a.deadline}")
    print()
```

### Validate Results

```python
from validators import validate_decisions, validate_actions

decision_report = validate_decisions(decisions)
print(f"Decision Issues: {decision_report['issue_count']}")

action_report = validate_actions(action_items)
print(f"Action Issues: {action_report['issue_count']}")
```

## 🛠️ Development Workflow

### 1. Make Changes

Edit any file in `agents/`, `validators/`, `api/`, etc.

### 2. Test Locally

```bash
# Restart the server
# It auto-reloads in DEBUG mode
python main.py
```

### 3. Test API

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"transcript_text": "..."}'
```

### 4. Check Logs

Logs are printed to console with timestamps and log levels.

## 📞 Troubleshooting

### "No module named 'config'"

```bash
# Ensure you're running from project root
cd patchamomma/
python main.py
```

### "GEMINI_API_KEY not found"

```bash
# Make sure .env file exists and is in root directory
cp .env.example .env
# Edit .env and add your API key
```

### "Connection refused" on API call

```bash
# Make sure backend is running
python main.py

# Check health
curl http://localhost:8000/health
```

### Gemini Returns Empty Decisions

- Check API key is valid
- Verify transcript is long enough (>50 chars)
- Check logs for Gemini API errors
- Try a different transcript

## 🚀 Next Steps

1. ✅ Backend setup and agents working
2. ⬜ Build React frontend
3. ⬜ Integrate with BigQuery (optional)
4. ⬜ Deploy to Cloud Run (optional)
5. ⬜ Create demo video

## 📚 Resources

- [Gemini API](https://ai.google.dev)
- [FastAPI](https://fastapi.tiangolo.com)
- [Pydantic](https://docs.pydantic.dev)
- [AMI Meeting Corpus](https://groups.inf.ed.ac.uk/ami/corpus/)
- [Google Cloud Run](https://cloud.google.com/run) (future deployment)

---

**Built for Patchamomma Hackathon**
**Last Updated**: August 26, 2024
