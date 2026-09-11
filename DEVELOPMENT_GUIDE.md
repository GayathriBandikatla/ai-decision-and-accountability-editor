# Patchamomma Development Guide

Quick reference for building the AI Decision & Accountability Auditor.

## 📋 Project Overview

**Goal**: Extract decisions, action items, owners, deadlines, and dependencies from meeting transcripts using Gemini agents.

**Tech Stack**: Python, Gemini 2.0 Flash, FastAPI, React, BigQuery, Cloud Storage, Firestore, Cloud Run

---

## 🚀 Quick Start

```bash
# 1. Setup
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your GEMINI_API_KEY

# 3. Download Data
python scripts/download_ami_corpus.py

# 4. Run Backend
python main.py

# 5. Run Frontend (in another terminal)
cd frontend && npm start
```

---

## 📦 Project Structure

```
patchamomma/
├── config/            # Settings, env loading
├── data_models/       # Pydantic models
├── agents/            # Gemini agents
├── validators/        # Deterministic validation
├── integrations/      # GCP clients (BigQuery, Firestore)
├── api/               # FastAPI routes
├── frontend/          # React app
├── tests/             # Unit + integration tests
├── scripts/           # Helper scripts
└── main.py            # Start backend server
```

---

## 🔄 Implementation Order

### Phase 1: Setup (30 min)
- [ ] Create venv, install deps, create .env
- [ ] Initialize folder structure
- [ ] Download AMI Corpus data (5 transcripts)

### Phase 2: Data Models (1 hour)
- [ ] Create Pydantic models: Transcript, Decision, ActionItem, Dependency
- [ ] Create config/settings.py for .env loading

### Phase 3: Agents (2 hours)
- [ ] Decision Extractor (Gemini 2.0 Flash)
- [ ] Action Item Extractor
- [ ] Dependency Mapper
- [ ] Test each agent locally

### Phase 4: Validators (1 hour)
- [ ] Decision validator (duplicates, confidence, evidence)
- [ ] Action validator (owner, deadline checks)
- [ ] Conflict detector (contradictions, circular deps)

### Phase 5: FastAPI Backend (1.5 hours)
- [ ] Setup FastAPI app
- [ ] Implement `/analyze` endpoint
- [ ] Add error handling, logging

### Phase 6: React Frontend (2 hours)
- [ ] Create React app
- [ ] UploadArea, ResultsPanel, EvidenceViewer components
- [ ] Styling (Tailwind or Material-UI)

### Phase 7: Cloud Integration (1 hour)
- [ ] BigQuery client (insert decisions, actions)
- [ ] Firestore client (decision ledger)
- [ ] Cloud Storage client (transcript archival)

### Phase 8: Docker (30 min)
- [ ] Dockerfile for backend
- [ ] docker-compose for local testing

### Phase 9: Testing & Demo (1 hour)
- [ ] Unit tests
- [ ] End-to-end demo script
- [ ] README documentation

**Total: ~10-12 hours**

---

## 🎛️ Key Files Explained

### `config/settings.py`
Loads environment variables from `.env`. Never hardcode secrets.

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    GCP_PROJECT_ID: str
    # ... more settings
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### `data_models/decision.py`
Example Pydantic model for decisions:

```python
from pydantic import BaseModel

class Decision(BaseModel):
    text: str
    confidence: float  # 0-1
    evidence_timestamp: Optional[str] = None
    evidence_speaker: Optional[str] = None
    evidence_text: str  # Full text excerpt
```

### `agents/decision_extractor.py`
Calls Gemini to extract decisions from transcript:

```python
def extract_decisions(transcript_text: str) -> List[Decision]:
    # Use Gemini 2.0 Flash with function calling
    # Return list of Decision objects
    pass
```

### `validators/decision_validator.py`
Deterministic validation (no Gemini):

```python
def validate_decisions(decisions: List[Decision]) -> ValidationReport:
    # Check duplicates (fuzzy match)
    # Check confidence (< 60% → flag)
    # Check evidence (missing → flag)
    # Return ValidationReport with issues
    pass
```

### `api/routes.py`
FastAPI endpoints:

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    # 1. Call Decision Extractor agent
    # 2. Call Action Extractor agent
    # 3. Call Dependency Mapper agent
    # 4. Run validators
    # 5. Insert into BigQuery
    # 6. Return results
    pass
```

### `frontend/src/App.jsx`
Main React component:

```jsx
export default function App() {
  const [transcript, setTranscript] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    const res = await fetch("/api/analyze", {
      method: "POST",
      body: JSON.stringify({ transcript_text: transcript })
    });
    setResults(await res.json());
    setLoading(false);
  };

  return (
    <div>
      <textarea value={transcript} onChange={(e) => setTranscript(e.target.value)} />
      <button onClick={handleAnalyze}>Analyze</button>
      {results && <ResultsPanel data={results} />}
    </div>
  );
}
```

---

## 📥 Downloading AMI Corpus Data

### Option 1: Automated Script (Recommended)
Create `scripts/download_ami_corpus.py`:

```python
import requests
import os
import json
from pathlib import Path

# AMI Corpus is publicly available
# You can download directly or parse from their website

def download_ami_corpus():
    """Download 5 sample AMI transcripts."""
    
    # Example: Download from AMI server or local mirror
    ami_urls = [
        "https://groups.inf.ed.ac.uk/ami/corpus/...",
        # ... more URLs
    ]
    
    output_dir = Path("tests/fixtures/sample_transcripts")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for url in ami_urls:
        # Download transcript
        # Parse XML to JSON format
        # Save to output_dir
        pass

if __name__ == "__main__":
    download_ami_corpus()
    print("✅ Downloaded 5 AMI transcripts")
```

### Option 2: Manual Download
1. Visit: https://groups.inf.ed.ac.uk/ami/corpus/
2. Download 5 meeting transcripts (XML or text format)
3. Place in `tests/fixtures/sample_transcripts/`
4. Use `scripts/parse_transcripts.py` to convert to JSON

### Option 3: Use Pre-Formatted Data
I've included sample JSON files in the repo with the structure you need.

---

## 🤖 Gemini Agent Integration

### Setup Gemini API
1. Go to [Google AI Studio](https://aistudio.google.com)
2. Create a new API key
3. Copy to `.env` as `GEMINI_API_KEY`

### Example: Call Gemini 2.0 Flash

```python
import google.generativeai as genai

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3.6-flash")

prompt = """Extract all decisions from this meeting transcript.
Return as JSON: { "decisions": [{ "text": "...", "confidence": 0.9 }] }

Transcript:
{transcript_text}
"""

response = model.generate_content(prompt)
# Parse response as JSON
decisions = parse_json_response(response.text)
```

---

## ☁️ Google Cloud Setup

### 1. Create GCP Project
```bash
gcloud projects create patchamomma
gcloud config set project patchamomma
```

### 2. Enable Services
```bash
gcloud services enable bigquery.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable storage-api.googleapis.com
gcloud services enable run.googleapis.com
```

### 3. Create Service Account
```bash
gcloud iam service-accounts create patchamomma-sa
gcloud projects add-iam-policy-binding patchamomma \
  --member="serviceAccount:patchamomma-sa@patchamomma.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"
```

### 4. Create BigQuery Dataset
```bash
bq mk --dataset \
  --description="Patchamomma decision ledger" \
  patchamomma
```

### 5. Add to `.env`
```
GCP_PROJECT_ID=patchamomma
GCP_CREDENTIALS_PATH=/path/to/service_account.json
```

---

## 🧪 Testing Locally

### 1. Test Individual Agent
```python
from agents.decision_extractor import extract_decisions

transcript = open("tests/fixtures/sample_transcripts/meeting1.json").read()
decisions = extract_decisions(transcript)
for d in decisions:
    print(f"- {d.text} (confidence: {d.confidence})")
```

### 2. Test Validators
```python
from validators.decision_validator import validate_decisions

validation = validate_decisions(decisions)
print(f"Issues: {validation.issues}")
```

### 3. Test Full API
```bash
# Start backend
python main.py

# In another terminal, test the endpoint
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"transcript_text": "..."}'
```

### 4. Test Frontend
```bash
cd frontend
npm start
# Opens http://localhost:3000
# Paste a transcript and click "Analyze"
```

---

## 📊 BigQuery Schema

### Table: `decisions`
```sql
CREATE TABLE `patchamomma.decisions` (
  decision_id STRING,
  meeting_id STRING,
  text STRING,
  confidence FLOAT64,
  evidence_timestamp STRING,
  evidence_speaker STRING,
  evidence_text STRING,
  created_at TIMESTAMP
);
```

### Table: `action_items`
```sql
CREATE TABLE `patchamomma.action_items` (
  action_id STRING,
  meeting_id STRING,
  text STRING,
  owner STRING,
  deadline DATE,
  priority STRING,
  status STRING,
  evidence_text STRING,
  created_at TIMESTAMP
);
```

---

## 🐳 Docker & Deployment

### Local Testing
```bash
docker-compose up
# Opens http://localhost:3000 (frontend) + http://localhost:8000 (backend)
```

### Deploy to Cloud Run
```bash
gcloud run deploy patchamomma --source . \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY \
  --set-env-vars GCP_PROJECT_ID=$GCP_PROJECT_ID \
  --allow-unauthenticated
```

---

## 🎥 Demo Script

Create `scripts/demo.py`:
```python
from pathlib import Path
from api.main import app
from agents.decision_extractor import extract_decisions
# ... imports

def demo():
    """End-to-end demo with all 5 sample transcripts."""
    
    transcripts = Path("tests/fixtures/sample_transcripts").glob("*.json")
    
    for transcript_file in transcripts:
        print(f"\n📄 Processing {transcript_file.name}...")
        
        # Load transcript
        # Extract decisions, actions, dependencies
        # Validate
        # Print results
        # Insert into BigQuery
        
        print("✅ Complete")

if __name__ == "__main__":
    demo()
```

Run with: `python scripts/demo.py`

---

## ✅ Checklist Before Submission

- [ ] All 5 transcripts process without errors
- [ ] `/analyze` endpoint handles edge cases
- [ ] No secrets in logs or responses
- [ ] BigQuery has decision/action data
- [ ] React frontend is responsive (mobile, tablet, desktop)
- [ ] Docker container builds and runs
- [ ] Cloud Run deployment works
- [ ] Demo video (3-5 min) recorded
- [ ] README complete
- [ ] Hackathon form submitted

---

## 🔗 Useful Links

- **Gemini API Docs**: https://ai.google.dev/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev
- **BigQuery Docs**: https://cloud.google.com/bigquery/docs
- **AMI Corpus**: https://groups.inf.ed.ac.uk/ami/corpus/

---

## ❓ Common Issues

### Gemini API Rate Limit
- Add exponential backoff retry logic
- Use caching for repeated transcripts

### Long Transcripts (> 10K tokens)
- Split into chunks
- Process in parallel
- Merge results

### BigQuery Permission Denied
- Verify service account has `BigQuery Data Editor` role
- Check credentials file path in `.env`

### React Component Not Updating
- Use `useState` properly
- Add `useEffect` for side effects
- Check API response format

---

## 📞 Need Help?

- Check DEVELOPMENT_GUIDE.md (this file)
- Review the plan file for architecture overview
- Test individual components in isolation
- Print debug logs to understand data flow

---

**Ready to build? Start with Phase 1: Project Setup!** 🚀
